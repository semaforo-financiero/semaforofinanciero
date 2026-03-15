<script setup lang="ts">
import { ref, computed, onMounted } from "vue";

import { toasterStore } from "../stores/toasterStore";
import api from "../lib/api";
import { useAuthStore } from "../stores/authStore";
import type Expense from "../lib/api/models/Expense";
import { STABILITY } from "../lib/api/models/Income";
import CurrencySimbol from "../assets/icons/CurrencySimbol.vue";
import Padlock from "../assets/icons/Padlock.vue";
import Pulse from "../assets/icons/Pulse.vue";
import Trash from "../assets/icons/Trash.vue";
import Spinner from "../components/atoms/Spinner.vue";
import PlusCircle from "../assets/icons/PlusCircle.vue";
import Check from "../assets/icons/Check.vue";

interface ExpenseAmount {
    expenseId: string;
    amount: number | null;
}

interface HistoricalRecord {
    id: string;
    month: number;
    year: number;
    totalAmount: number;
    filledAt: string;
}

const authStore = useAuthStore();

const expenses = ref<Expense[]>([]);
const expenseAmounts = ref<ExpenseAmount[]>([]);
const historicalRecords = ref<HistoricalRecord[]>([]);

const isLoading = ref(true);
const showCreateForm = ref(false);
const isCreating = ref(false);
const removingExpenseId = ref<string | null>(null);
const isSavingAmounts = ref(false);

const newExpense = ref<Expense>({
    name: "",
    stability: STABILITY.FIXED,
    is_debt: false,
    description: "",
});

const currentDate = new Date();
const currentMonth = currentDate.getMonth();
const currentYear = currentDate.getFullYear();

const monthNames = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
];

const currentMonthYear = computed(() => {
    return `${monthNames[currentMonth]} ${currentYear}`;
});

const getMonthYearLabel = (month: number, year: number) => {
    return `${monthNames[month]} ${year}`;
};

const getExpenseById = (id: string) => {
    return expenses.value.find((e) => e.id === id);
};

const getAmountForExpense = (expenseId: string) => {
    const found = expenseAmounts.value.find((a) => a.expenseId === expenseId);
    return found?.amount ?? null;
};

const setAmountForExpense = (expenseId: string, value: string) => {
    const numValue = value === "" ? null : parseFloat(value);
    const existing = expenseAmounts.value.find(
        (a) => a.expenseId === expenseId,
    );
    if (existing) {
        existing.amount = numValue;
    } else {
        expenseAmounts.value.push({ expenseId, amount: numValue });
    }
};

const fetchData = async () => {
    isLoading.value = true;
    try {
        const token = authStore.getAccessToken();

        if (!token) {
            throw new Error("No se encontró el token de autenticación");
        }

        expenses.value = await api.expense.get(token);

        expenses.value = expenses.value.filter((expense) => expense.is_active);

        // Mock current month amounts
        expenseAmounts.value = [
            { expenseId: "1", amount: 15000 },
            { expenseId: "2", amount: null },
            { expenseId: "3", amount: 500 },
        ];

        // Mock historical records
        historicalRecords.value = [
            {
                id: "h1",
                month: 1,
                year: 2026,
                totalAmount: 16200,
                filledAt: "2026-02-01",
            },
            {
                id: "h2",
                month: 0,
                year: 2026,
                totalAmount: 15800,
                filledAt: "2026-01-02",
            },
            {
                id: "h3",
                month: 11,
                year: 2025,
                totalAmount: 18500,
                filledAt: "2025-12-01",
            },
            {
                id: "h4",
                month: 10,
                year: 2025,
                totalAmount: 15000,
                filledAt: "2025-11-02",
            },
        ];
    } catch (error) {
        toasterStore.error(
            "Error innesperado.",
            "No se pudieron cargar los egresos. Intenta de nuevo más tarde.",
        );
    } finally {
        isLoading.value = false;
    }
};

const createExpense = async () => {
    if (!newExpense.value.name.trim()) {
        return;
    }

    isCreating.value = true;

    try {
        const token = authStore.getAccessToken();

        if (!token) {
            throw new Error("No se encontró el token de autenticación");
        }

        const created: Expense = {
            name: newExpense.value.name,
            stability: newExpense.value.stability,
            description: newExpense.value.description,
        };

        const expenseIdCreated = await api.expense.create(created, token);

        created.id = expenseIdCreated;
        expenses.value.push(created);

        expenseAmounts.value.push({
            expenseId: expenseIdCreated,
            amount: null,
        });

        newExpense.value = {
            name: "",
            stability: STABILITY.FIXED,
            description: "",
        };

        showCreateForm.value = false;

        toasterStore.success(
            "Egreso creado",
            `El egreso "${created.name}" ha sido creado.`,
        );
    } catch (error) {
        toasterStore.error(
            "Error al crear el egreso.",
            "No se pudo crear el egreso. Intenta de nuevo más tarde.",
        );
    } finally {
        isCreating.value = false;
    }
};

const removeExpense = async (expense: Expense) => {
    removingExpenseId.value = expense.id!;

    try {
        const token = authStore.getAccessToken();

        if (!token) {
            throw new Error("No se encontró el token de autenticación");
        }

        await api.expense.delete(expense.id!, token);

        expenses.value = expenses.value.filter((e) => e.id !== expense.id);

        expenseAmounts.value = expenseAmounts.value.filter(
            (a) => a.expenseId !== expense.id,
        );

        toasterStore.success(
            "Egreso eliminado",
            `El egreso "${expense.name}" ha sido eliminado.`,
        );
    } catch (error) {
        toasterStore.error(
            "Error al eliminar el egreso.",
            "No se pudo eliminar el egreso. Intenta de nuevo más tarde.",
        );
    } finally {
        removingExpenseId.value = null;
    }
};

// Save amounts
const saveAmounts = async () => {
    isSavingAmounts.value = true;

    try {
        // TODO: Replace with actual API call
        await new Promise((resolve) => setTimeout(resolve, 800));

        toasterStore.success(
            "Montos guardados",
            "Los montos de egresos han sido actualizados.",
        );
    } catch (error) {
        toasterStore.error(
            "Error al guardar los montos.",
            "No se pudieron guardar los montos. Intenta de nuevo más tarde.",
        );
    } finally {
        isSavingAmounts.value = false;
    }
};

const cancelCreate = () => {
    showCreateForm.value = false;
    newExpense.value = { name: "", stability: "FIXED", description: "" };
};

const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("es-MX", {
        style: "currency",
        currency: "MXN",
    }).format(amount);
};

onMounted(() => {
    fetchData();
});
</script>

<template>
    <div class="expense-view">
        <template v-if="isLoading">
            <div class="expense-grid">
                <div class="skeleton-card">
                    <div class="skeleton skeleton--title"></div>
                    <div
                        v-for="i in 3"
                        class="skeleton skeleton--item"
                        :key="i"
                    ></div>
                </div>
                <div class="skeleton-card">
                    <div class="skeleton skeleton--title"></div>
                    <div
                        v-for="i in 3"
                        class="skeleton skeleton--item"
                        :key="i"
                    ></div>
                </div>
            </div>
        </template>

        <template v-else>
            <div class="expense-grid">
                <div class="panel panel--left">
                    <div class="panel__header">
                        <div class="panel__header-left">
                            <div class="panel__icon panel__icon--primary">
                                <CurrencySimbol />
                            </div>
                            <div>
                                <h2 class="panel__title">Egresos</h2>
                                <p class="panel__subtitle">
                                    Gestiona tus egresos
                                </p>
                            </div>
                        </div>
                    </div>

                    <div v-if="expenses.length > 0" class="expense-list">
                        <TransitionGroup name="expense">
                            <div
                                v-for="expense in expenses"
                                :key="expense.id"
                                class="expense-item"
                                :class="{
                                    'expense-item--removing':
                                        removingExpenseId === expense.id,
                                }"
                            >
                                <div class="expense-item__left">
                                    <div
                                        class="expense-item__icon"
                                        :class="
                                            expense.stability ===
                                            STABILITY.FIXED
                                                ? 'expense-item__icon--fixed'
                                                : 'expense-item__icon--variable'
                                        "
                                    >
                                        <Padlock
                                            v-if="
                                                expense.stability ===
                                                STABILITY.FIXED
                                            "
                                        />
                                        <Pulse v-else />
                                    </div>
                                    <div class="expense-item__info">
                                        <div class="expense-item__name-row">
                                            <span class="expense-item__name">{{
                                                expense.name
                                            }}</span>
                                            <span
                                                class="expense-item__badge"
                                                :class="
                                                    expense.stability ===
                                                    STABILITY.FIXED
                                                        ? 'expense-item__badge--fixed'
                                                        : 'expense-item__badge--variable'
                                                "
                                            >
                                                {{
                                                    expense.stability ===
                                                    STABILITY.FIXED
                                                        ? "Fijo"
                                                        : "Variable"
                                                }}
                                            </span>
                                        </div>
                                        <span
                                            class="expense-item__description"
                                            >{{
                                                expense.description ||
                                                "Sin descripcion"
                                            }}</span
                                        >
                                    </div>
                                </div>
                                <button
                                    class="expense-item__remove"
                                    :disabled="removingExpenseId === expense.id"
                                    :title="`Eliminar ${expense.name}`"
                                    @click="removeExpense(expense)"
                                >
                                    <Trash
                                        v-if="removingExpenseId !== expense.id"
                                    />
                                    <Spinner v-else />
                                </button>
                            </div>
                        </TransitionGroup>
                    </div>

                    <div v-else-if="!showCreateForm" class="empty-state">
                        <div class="empty-state__icon"><CurrencySimbol /></div>
                        <p class="empty-state__text">
                            No hay egresos registrados
                        </p>
                        <p class="empty-state__sub">
                            Crea tu primer egreso para comenzar
                        </p>
                    </div>

                    <Transition name="slide">
                        <div v-if="showCreateForm" class="create-form">
                            <div class="create-form__header">
                                <PlusCircle />
                                <span>Nuevo egreso</span>
                            </div>

                            <div class="create-form__field">
                                <label class="create-form__label">Nombre</label>
                                <div class="create-form__input-wrapper">
                                    <input
                                        v-model="newExpense.name"
                                        type="text"
                                        class="create-form__input"
                                        placeholder="Ej: Salario, Freelance..."
                                    />
                                </div>
                            </div>

                            <div class="create-form__field">
                                <label class="create-form__label"
                                    >Tipo de egreso</label
                                >
                                <div class="create-form__type-selector">
                                    <button
                                        type="button"
                                        class="create-form__type-btn"
                                        :class="{
                                            'create-form__type-btn--active':
                                                newExpense.stability ===
                                                STABILITY.FIXED,
                                        }"
                                        @click="
                                            newExpense.stability =
                                                STABILITY.FIXED
                                        "
                                    >
                                        <Padlock />
                                        Fijo
                                    </button>
                                    <button
                                        type="button"
                                        class="create-form__type-btn"
                                        :class="{
                                            'create-form__type-btn--active':
                                                newExpense.stability ===
                                                STABILITY.VARIABLE,
                                        }"
                                        @click="
                                            newExpense.stability =
                                                STABILITY.VARIABLE
                                        "
                                    >
                                        <Pulse />
                                        Variable
                                    </button>
                                </div>
                            </div>

                            <div class="create-form__field">
                                <label class="create-form__label"
                                    >Descripcion (opcional)</label
                                >
                                <textarea
                                    v-model="newExpense.description"
                                    class="create-form__textarea"
                                    placeholder="Breve descripcion del egreso..."
                                    rows="2"
                                ></textarea>
                            </div>

                            <div class="create-form__actions">
                                <button
                                    class="create-form__btn create-form__btn--cancel"
                                    @click="cancelCreate"
                                >
                                    Cancelar
                                </button>
                                <button
                                    class="create-form__btn create-form__btn--submit"
                                    :disabled="
                                        isCreating || !newExpense.name.trim()
                                    "
                                    @click="createExpense"
                                >
                                    <Check v-if="!isCreating" />
                                    <Spinner v-else />
                                    {{
                                        isCreating
                                            ? "Creando..."
                                            : "Crear egreso"
                                    }}
                                </button>
                            </div>
                        </div>
                    </Transition>

                    <button
                        v-if="!showCreateForm"
                        class="create-btn"
                        @click="showCreateForm = true"
                    >
                        <PlusCircle />
                        Crear egreso
                    </button>

                    <div class="panel__accent">
                        <div
                            class="panel__accent-segment panel__accent-segment--green-light"
                        ></div>
                    </div>
                </div>

                <!-- RIGHT PANEL: Expense Amounts -->
                <div class="panel panel--right">
                    <div class="panel__header">
                        <div class="panel__header-left">
                            <div class="panel__icon panel__icon--secondary">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    width="22"
                                    height="22"
                                >
                                    <rect
                                        x="3"
                                        y="4"
                                        width="18"
                                        height="18"
                                        rx="2"
                                        ry="2"
                                    />
                                    <line x1="16" y1="2" x2="16" y2="6" />
                                    <line x1="8" y1="2" x2="8" y2="6" />
                                    <line x1="3" y1="10" x2="21" y2="10" />
                                </svg>
                            </div>
                            <div>
                                <h2 class="panel__title">Monto de egresos</h2>
                                <p
                                    class="panel__subtitle panel__subtitle--highlight"
                                >
                                    {{ currentMonthYear }}
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Amount Inputs -->
                    <div v-if="expenses.length > 0" class="amounts-section">
                        <div class="amounts-list">
                            <div
                                v-for="expense in expenses"
                                :key="expense.id"
                                class="amount-row"
                            >
                                <div class="amount-row__label">
                                    <span class="amount-row__name">{{
                                        expense.name
                                    }}</span>
                                    <span
                                        class="amount-row__type"
                                        :class="
                                            expense.stability ===
                                            STABILITY.FIXED
                                                ? 'amount-row__type--fixed'
                                                : 'amount-row__type--variable'
                                        "
                                    >
                                        {{
                                            expense.stability ===
                                            STABILITY.FIXED
                                                ? "Fijo"
                                                : "Variable"
                                        }}
                                    </span>
                                </div>
                                <div class="amount-row__input-wrapper">
                                    <span class="amount-row__currency">$</span>
                                    <input
                                        type="number"
                                        class="amount-row__input"
                                        placeholder="0.00"
                                        :value="
                                            getAmountForExpense(expense.id!)
                                        "
                                        @input="
                                            (e) =>
                                                setAmountForExpense(
                                                    expense.id!,
                                                    (
                                                        e.target as HTMLInputElement
                                                    ).value,
                                                )
                                        "
                                    />
                                </div>
                            </div>
                        </div>

                        <button
                            class="save-btn"
                            :disabled="isSavingAmounts"
                            @click="saveAmounts"
                        >
                            <svg
                                v-if="!isSavingAmounts"
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                width="18"
                                height="18"
                            >
                                <path
                                    d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"
                                />
                                <polyline points="17 21 17 13 7 13 7 21" />
                                <polyline points="7 3 7 8 15 8" />
                            </svg>
                            <svg
                                v-else
                                class="spinner"
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                width="18"
                                height="18"
                            >
                                <circle
                                    cx="12"
                                    cy="12"
                                    r="10"
                                    stroke-dasharray="30 70"
                                />
                            </svg>
                            {{
                                isSavingAmounts
                                    ? "Guardando..."
                                    : "Guardar montos"
                            }}
                        </button>
                    </div>

                    <!-- No expenses message -->
                    <div v-else class="amounts-empty">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="1.5"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            width="32"
                            height="32"
                        >
                            <circle cx="12" cy="12" r="10" />
                            <line x1="12" y1="16" x2="12" y2="12" />
                            <line x1="12" y1="8" x2="12.01" y2="8" />
                        </svg>
                        <p>
                            Crea tus egresos primero para poder registrar los
                            montos
                        </p>
                    </div>

                    <!-- Historical Records -->
                    <div class="historical-section">
                        <div class="historical-section__header">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                width="18"
                                height="18"
                            >
                                <circle cx="12" cy="12" r="10" />
                                <polyline points="12 6 12 12 16 14" />
                            </svg>
                            <h3>Historico de egresos</h3>
                        </div>

                        <div
                            v-if="historicalRecords.length > 0"
                            class="historical-list"
                        >
                            <button
                                v-for="record in historicalRecords"
                                :key="record.id"
                                class="historical-item"
                            >
                                <div class="historical-item__left">
                                    <div class="historical-item__icon">
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            stroke-width="2"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            width="16"
                                            height="16"
                                        >
                                            <rect
                                                x="3"
                                                y="4"
                                                width="18"
                                                height="18"
                                                rx="2"
                                                ry="2"
                                            />
                                            <line
                                                x1="16"
                                                y1="2"
                                                x2="16"
                                                y2="6"
                                            />
                                            <line x1="8" y1="2" x2="8" y2="6" />
                                            <line
                                                x1="3"
                                                y1="10"
                                                x2="21"
                                                y2="10"
                                            />
                                        </svg>
                                    </div>
                                    <div class="historical-item__info">
                                        <span class="historical-item__month">{{
                                            getMonthYearLabel(
                                                record.month,
                                                record.year,
                                            )
                                        }}</span>
                                        <span class="historical-item__date"
                                            >Registrado el
                                            {{
                                                new Date(
                                                    record.filledAt,
                                                ).toLocaleDateString("es-MX")
                                            }}</span
                                        >
                                    </div>
                                </div>
                                <div class="historical-item__right">
                                    <span class="historical-item__amount">{{
                                        formatCurrency(record.totalAmount)
                                    }}</span>
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="2"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        width="16"
                                        height="16"
                                    >
                                        <polyline points="9 18 15 12 9 6" />
                                    </svg>
                                </div>
                            </button>
                        </div>

                        <div v-else class="historical-empty">
                            <p>No hay registros historicos aun</p>
                        </div>
                    </div>

                    <!-- Decorative bar -->
                    <div class="panel__accent">
                        <div
                            class="panel__accent-segment panel__accent-segment--blue"
                        ></div>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<style scoped>
.expense-view {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 1100px;
    margin: 2.5rem auto;
    padding: 0 1.5rem;
}

.expense-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
}

@media (min-width: 860px) {
    .expense-grid {
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
    }
}

.panel {
    position: relative;
    z-index: 1;
    background: var(--color-white, #fff);
    border-radius: 20px;
    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.06),
        0 8px 24px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.04);
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.panel__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 1.75rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.panel__header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.panel__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    min-width: 48px;
    border-radius: 14px;
    color: var(--color-white, #fff);
}
.panel__icon--primary {
    background: linear-gradient(
        135deg,
        var(--primary-color, #43a047),
        var(--primary-color-light, #66bb6a)
    );
    box-shadow: 0 4px 12px rgba(67, 160, 71, 0.3);
}
.panel__icon--secondary {
    background: linear-gradient(
        135deg,
        var(--secondary-color, #006285),
        var(--secondary-color-dark, #004c6d)
    );
    box-shadow: 0 4px 12px rgba(0, 98, 133, 0.3);
}

.panel__title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-color, #212121);
    line-height: 1.25;
}

.panel__subtitle {
    font-size: 0.82rem;
    color: var(--neutral-light, #6b7280);
    margin-top: 0.15rem;
}

.panel__subtitle--highlight {
    color: var(--secondary-color, #006285);
    font-weight: 600;
}

.panel__accent {
    display: flex;
    height: 4px;
    margin-top: auto;
}
.panel__accent-segment {
    flex: 1;
}
.panel__accent-segment--green {
    background: var(--primary-color, #43a047);
}
.panel__accent-segment--blue {
    background: var(--secondary-color, #006285);
}
.panel__accent-segment--green-light {
    background: var(--primary-color-light, #66bb6a);
}

.expense-list {
    padding: 0.5rem 0;
}

.expense-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.75rem;
    transition:
        background 0.15s,
        opacity 0.3s;
}
.expense-item:hover {
    background: rgba(0, 0, 0, 0.015);
}
.expense-item--removing {
    opacity: 0.4;
    pointer-events: none;
}

.expense-item__left {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    min-width: 0;
}

.expense-item__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    min-width: 40px;
    border-radius: 10px;
}
.expense-item__icon--fixed {
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color, #43a047);
}
.expense-item__icon--variable {
    background: rgba(0, 98, 133, 0.1);
    color: var(--secondary-color, #006285);
}

.expense-item__info {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    min-width: 0;
}

.expense-item__name-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.expense-item__name {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-color, #212121);
}

.expense-item__badge {
    padding: 0.12rem 0.5rem;
    border-radius: 5px;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
.expense-item__badge--fixed {
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color-dark, #388e3c);
}
.expense-item__badge--variable {
    background: rgba(0, 98, 133, 0.1);
    color: var(--secondary-color, #006285);
}

.expense-item__description {
    font-size: 0.78rem;
    color: var(--neutral-light, #6b7280);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.expense-item__remove {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--neutral-light, #6b7280);
    cursor: pointer;
    transition: all 0.15s;
    flex-shrink: 0;
}
.expense-item__remove:hover:not(:disabled) {
    background: rgba(211, 47, 47, 0.08);
    color: #c62828;
}

.expense-enter-active,
.expense-leave-active {
    transition: all 0.3s ease;
}
.expense-enter-from {
    opacity: 0;
    transform: translateX(-12px);
}
.expense-leave-to {
    opacity: 0;
    transform: translateX(12px);
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2.5rem 1.5rem;
    text-align: center;
}
.empty-state__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 16px;
    background: rgba(67, 160, 71, 0.08);
    color: var(--primary-color, #43a047);
    margin-bottom: 1rem;
}
.empty-state__text {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-color, #212121);
    margin-bottom: 0.25rem;
}
.empty-state__sub {
    font-size: 0.82rem;
    color: var(--neutral-light, #6b7280);
}

.create-form {
    padding: 1.25rem 1.75rem;
    background: rgba(67, 160, 71, 0.03);
    border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.create-form__header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--primary-color-dark, #388e3c);
    margin-bottom: 1rem;
}

.create-form__field {
    margin-bottom: 1rem;
}

.create-form__label {
    display: block;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-color, #212121);
    margin-bottom: 0.4rem;
}

.create-form__input-wrapper {
    display: flex;
    align-items: center;
    height: 42px;
    border-radius: 10px;
    border: 2px solid var(--color-gray-light, #dedede);
    background: var(--color-white, #fff);
    transition:
        border-color 0.2s,
        box-shadow 0.2s;
    overflow: hidden;
}
.create-form__input-wrapper:focus-within {
    border-color: var(--primary-color, #43a047);
    box-shadow: 0 0 0 3px rgba(67, 160, 71, 0.12);
}

.create-form__input {
    flex: 1;
    height: 100%;
    border: none;
    outline: none;
    padding: 0 1rem;
    font-size: 0.88rem;
    font-family: inherit;
    color: var(--text-color, #212121);
    background: transparent;
}
.create-form__input::placeholder {
    color: #b0b0b0;
}

.create-form__textarea {
    width: 100%;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    border: 2px solid var(--color-gray-light, #dedede);
    background: var(--color-white, #fff);
    font-size: 0.88rem;
    font-family: inherit;
    color: var(--text-color, #212121);
    resize: vertical;
    transition:
        border-color 0.2s,
        box-shadow 0.2s;
}
.create-form__textarea:focus {
    outline: none;
    border-color: var(--primary-color, #43a047);
    box-shadow: 0 0 0 3px rgba(67, 160, 71, 0.12);
}
.create-form__textarea::placeholder {
    color: #b0b0b0;
}

.create-form__type-selector {
    display: flex;
    gap: 0.75rem;
}

.create-form__type-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    height: 42px;
    border-radius: 10px;
    border: 2px solid var(--color-gray-light, #dedede);
    background: var(--color-white, #fff);
    font-size: 0.85rem;
    font-weight: 600;
    font-family: inherit;
    color: var(--neutral-light, #6b7280);
    cursor: pointer;
    transition: all 0.2s;
}
.create-form__type-btn:hover {
    border-color: var(--primary-color, #43a047);
    color: var(--primary-color, #43a047);
}
.create-form__type-btn--active {
    border-color: var(--primary-color, #43a047);
    background: rgba(67, 160, 71, 0.08);
    color: var(--primary-color-dark, #388e3c);
}

.create-form__actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 1.25rem;
}

.create-form__btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    height: 42px;
    border-radius: 10px;
    font-size: 0.88rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.15s;
}

.create-form__btn--cancel {
    border: 2px solid var(--color-gray-light, #dedede);
    background: transparent;
    color: var(--neutral-light, #6b7280);
}
.create-form__btn--cancel:hover {
    border-color: #b0b0b0;
    background: rgba(0, 0, 0, 0.02);
}

.create-form__btn--submit {
    border: none;
    background: linear-gradient(
        135deg,
        var(--primary-color, #43a047),
        var(--primary-color-dark, #388e3c)
    );
    color: var(--color-white, #fff);
    box-shadow: 0 4px 12px rgba(67, 160, 71, 0.3);
}
.create-form__btn--submit:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(67, 160, 71, 0.4);
}
.create-form__btn--submit:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.slide-enter-active {
    transition: all 0.3s ease;
}
.slide-leave-active {
    transition: all 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
    opacity: 0;
    max-height: 0;
}

.create-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin: 1rem 1.75rem 1.5rem;
    padding: 0.85rem;
    border-radius: 12px;
    border: 2px dashed rgba(67, 160, 71, 0.3);
    background: rgba(67, 160, 71, 0.04);
    color: var(--primary-color, #43a047);
    font-size: 0.9rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s;
}
.create-btn:hover {
    border-color: var(--primary-color, #43a047);
    background: rgba(67, 160, 71, 0.08);
}

.amounts-section {
    padding: 1.25rem 1.75rem;
}

.amounts-list {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    margin-bottom: 1.25rem;
}

.amount-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.amount-row__label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    min-width: 0;
}

.amount-row__name {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-color, #212121);
}

.amount-row__type {
    padding: 0.1rem 0.45rem;
    border-radius: 4px;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
}
.amount-row__type--fixed {
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color-dark, #388e3c);
}
.amount-row__type--variable {
    background: rgba(0, 98, 133, 0.1);
    color: var(--secondary-color, #006285);
}

.amount-row__input-wrapper {
    display: flex;
    align-items: center;
    width: 140px;
    height: 40px;
    border-radius: 10px;
    border: 2px solid var(--color-gray-light, #dedede);
    background: var(--color-white, #fff);
    overflow: hidden;
    transition:
        border-color 0.2s,
        box-shadow 0.2s;
}
.amount-row__input-wrapper:focus-within {
    border-color: var(--secondary-color, #006285);
    box-shadow: 0 0 0 3px rgba(0, 98, 133, 0.12);
}

.amount-row__currency {
    padding: 0 0.5rem 0 0.75rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--neutral-light, #6b7280);
}

.amount-row__input {
    flex: 1;
    height: 100%;
    border: none;
    outline: none;
    font-size: 0.9rem;
    font-family: inherit;
    font-weight: 600;
    color: var(--text-color, #212121);
    background: transparent;
    padding-right: 0.75rem;
}
.amount-row__input::placeholder {
    color: #c0c0c0;
    font-weight: 400;
}
.amount-row__input::-webkit-outer-spin-button,
.amount-row__input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
.amount-row__input[type="number"] {
    -moz-appearance: textfield;
}

.save-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    width: 100%;
    height: 44px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(
        135deg,
        var(--secondary-color, #006285),
        var(--secondary-color-dark, #004c6d)
    );
    color: var(--color-white, #fff);
    font-size: 0.9rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 98, 133, 0.3);
    transition: all 0.15s;
}
.save-btn:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 98, 133, 0.4);
}
.save-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.amounts-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    padding: 2rem 1.5rem;
    text-align: center;
    color: var(--neutral-light, #6b7280);
}
.amounts-empty p {
    font-size: 0.85rem;
    line-height: 1.4;
}

.historical-section {
    border-top: 1px solid rgba(0, 0, 0, 0.05);
    padding: 1.25rem 1.75rem;
}

.historical-section__header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    color: var(--text-color, #212121);
}
.historical-section__header h3 {
    font-size: 0.95rem;
    font-weight: 700;
}

.historical-list {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
}

.historical-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 0.9rem 1rem;
    border-radius: 12px;
    border: 1px solid rgba(0, 0, 0, 0.06);
    background: var(--background-color, #f7f7f7);
    cursor: pointer;
    transition: all 0.15s;
    text-align: left;
}
.historical-item:hover {
    background: rgba(0, 98, 133, 0.04);
    border-color: rgba(0, 98, 133, 0.15);
}

.historical-item__left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.historical-item__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 9px;
    background: rgba(0, 98, 133, 0.08);
    color: var(--secondary-color, #006285);
}

.historical-item__info {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
}

.historical-item__month {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-color, #212121);
}

.historical-item__date {
    font-size: 0.75rem;
    color: var(--neutral-light, #6b7280);
}

.historical-item__right {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--neutral-light, #6b7280);
}

.historical-item__amount {
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--primary-color-dark, #388e3c);
}

.historical-empty {
    padding: 1.5rem;
    text-align: center;
    color: var(--neutral-light, #6b7280);
    font-size: 0.85rem;
}

.skeleton-card {
    position: relative;
    z-index: 1;
    background: var(--color-white, #fff);
    border-radius: 20px;
    padding: 2rem;
    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.06),
        0 8px 24px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.04);
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.skeleton {
    border-radius: 8px;
    background: linear-gradient(
        90deg,
        rgba(0, 0, 0, 0.04) 25%,
        rgba(0, 0, 0, 0.08) 50%,
        rgba(0, 0, 0, 0.04) 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
}
.skeleton--title {
    height: 24px;
    width: 50%;
}
.skeleton--item {
    height: 48px;
    width: 100%;
    border-radius: 10px;
}

@keyframes shimmer {
    0% {
        background-position: -200% 0;
    }
    100% {
        background-position: 200% 0;
    }
}

.spinner {
    animation: spin 1s linear infinite;
}
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>
