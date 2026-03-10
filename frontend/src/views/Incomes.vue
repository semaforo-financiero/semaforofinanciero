<script setup lang="ts">
import { ref, computed, onMounted } from "vue";

interface Income {
    id: string;
    name: string;
    type: "fixed" | "variable";
    description: string;
}

interface IncomeAmount {
    incomeId: string;
    amount: number | null;
}

interface HistoricalRecord {
    id: string;
    month: number;
    year: number;
    totalAmount: number;
    filledAt: string;
}

// State
const incomes = ref<Income[]>([]);
const incomeAmounts = ref<IncomeAmount[]>([]);
const historicalRecords = ref<HistoricalRecord[]>([]);

const isLoading = ref(true);
const showCreateForm = ref(false);
const isCreating = ref(false);
const removingIncomeId = ref<string | null>(null);
const isSavingAmounts = ref(false);

// Form state
const newIncome = ref({
    name: "",
    type: "fixed" as "fixed" | "variable",
    description: "",
});

// Messages
const errorMessage = ref("");
const successMessage = ref("");

// Current month/year
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

const getIncomeById = (id: string) => {
    return incomes.value.find((i) => i.id === id);
};

const getAmountForIncome = (incomeId: string) => {
    const found = incomeAmounts.value.find((a) => a.incomeId === incomeId);
    return found?.amount ?? null;
};

const setAmountForIncome = (incomeId: string, value: string) => {
    const numValue = value === "" ? null : parseFloat(value);
    const existing = incomeAmounts.value.find((a) => a.incomeId === incomeId);
    if (existing) {
        existing.amount = numValue;
    } else {
        incomeAmounts.value.push({ incomeId, amount: numValue });
    }
};

// Fetch data
const fetchData = async () => {
    isLoading.value = true;
    try {
        // TODO: Replace with actual API calls
        await new Promise((resolve) => setTimeout(resolve, 800));

        // Mock incomes
        incomes.value = [
            {
                id: "1",
                name: "Salario",
                type: "fixed",
                description: "Sueldo mensual de trabajo",
            },
            {
                id: "2",
                name: "Freelance",
                type: "variable",
                description: "Proyectos independientes",
            },
            {
                id: "3",
                name: "Inversiones",
                type: "variable",
                description: "Rendimientos de inversiones",
            },
        ];

        // Mock current month amounts
        incomeAmounts.value = [
            { incomeId: "1", amount: 15000 },
            { incomeId: "2", amount: null },
            { incomeId: "3", amount: 500 },
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
        errorMessage.value = "Error al cargar los datos.";
    } finally {
        isLoading.value = false;
    }
};

// Create income
const createIncome = async () => {
    if (!newIncome.value.name.trim()) return;
    isCreating.value = true;
    errorMessage.value = "";

    try {
        // TODO: Replace with actual API call
        await new Promise((resolve) => setTimeout(resolve, 600));

        const created: Income = {
            id: String(Date.now()),
            name: newIncome.value.name,
            type: newIncome.value.type,
            description: newIncome.value.description,
        };

        incomes.value.push(created);
        incomeAmounts.value.push({ incomeId: created.id, amount: null });

        // Reset form
        newIncome.value = { name: "", type: "fixed", description: "" };
        showCreateForm.value = false;

        successMessage.value = "Ingreso creado exitosamente.";
        setTimeout(() => {
            successMessage.value = "";
        }, 4000);
    } catch (error) {
        errorMessage.value = "Error al crear el ingreso.";
    } finally {
        isCreating.value = false;
    }
};

// Remove income
const removeIncome = async (income: Income) => {
    removingIncomeId.value = income.id;
    errorMessage.value = "";

    try {
        // TODO: Replace with actual API call
        await new Promise((resolve) => setTimeout(resolve, 500));

        incomes.value = incomes.value.filter((i) => i.id !== income.id);
        incomeAmounts.value = incomeAmounts.value.filter(
            (a) => a.incomeId !== income.id,
        );

        successMessage.value = `"${income.name}" eliminado.`;
        setTimeout(() => {
            successMessage.value = "";
        }, 4000);
    } catch (error) {
        errorMessage.value = "Error al eliminar el ingreso.";
    } finally {
        removingIncomeId.value = null;
    }
};

// Save amounts
const saveAmounts = async () => {
    isSavingAmounts.value = true;
    errorMessage.value = "";

    try {
        // TODO: Replace with actual API call
        await new Promise((resolve) => setTimeout(resolve, 800));

        successMessage.value = "Montos guardados exitosamente.";
        setTimeout(() => {
            successMessage.value = "";
        }, 4000);
    } catch (error) {
        errorMessage.value = "Error al guardar los montos.";
    } finally {
        isSavingAmounts.value = false;
    }
};

const cancelCreate = () => {
    showCreateForm.value = false;
    newIncome.value = { name: "", type: "fixed", description: "" };
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
    <div class="incomes-view">
        <!-- Alerts -->
        <Transition name="alert">
            <div v-if="successMessage" class="alert alert--success">
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
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                    <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
                <span>{{ successMessage }}</span>
            </div>
        </Transition>
        <Transition name="alert">
            <div v-if="errorMessage" class="alert alert--error">
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
                    <line x1="15" y1="9" x2="9" y2="15" />
                    <line x1="9" y1="9" x2="15" y2="15" />
                </svg>
                <span>{{ errorMessage }}</span>
                <button class="alert__close" @click="errorMessage = ''">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        width="14"
                        height="14"
                    >
                        <line x1="18" y1="6" x2="6" y2="18" />
                        <line x1="6" y1="6" x2="18" y2="18" />
                    </svg>
                </button>
            </div>
        </Transition>

        <!-- Loading -->
        <template v-if="isLoading">
            <div class="incomes-grid">
                <div class="skeleton-card">
                    <div class="skeleton skeleton--title"></div>
                    <div
                        class="skeleton skeleton--item"
                        v-for="i in 3"
                        :key="i"
                    ></div>
                </div>
                <div class="skeleton-card">
                    <div class="skeleton skeleton--title"></div>
                    <div
                        class="skeleton skeleton--item"
                        v-for="i in 3"
                        :key="i"
                    ></div>
                </div>
            </div>
        </template>

        <!-- Main Content -->
        <template v-else>
            <div class="incomes-grid">
                <!-- LEFT PANEL: Income Management -->
                <div class="panel panel--left">
                    <div class="panel__header">
                        <div class="panel__header-left">
                            <div class="panel__icon panel__icon--primary">
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
                                    <line x1="12" y1="1" x2="12" y2="23" />
                                    <path
                                        d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"
                                    />
                                </svg>
                            </div>
                            <div>
                                <h2 class="panel__title">Ingresos</h2>
                                <p class="panel__subtitle">
                                    Gestiona tus fuentes de ingreso
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Income List -->
                    <div v-if="incomes.length > 0" class="income-list">
                        <TransitionGroup name="income">
                            <div
                                v-for="income in incomes"
                                :key="income.id"
                                class="income-item"
                                :class="{
                                    'income-item--removing':
                                        removingIncomeId === income.id,
                                }"
                            >
                                <div class="income-item__left">
                                    <div
                                        class="income-item__icon"
                                        :class="
                                            income.type === 'fixed'
                                                ? 'income-item__icon--fixed'
                                                : 'income-item__icon--variable'
                                        "
                                    >
                                        <svg
                                            v-if="income.type === 'fixed'"
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
                                            <rect
                                                x="3"
                                                y="11"
                                                width="18"
                                                height="11"
                                                rx="2"
                                                ry="2"
                                            />
                                            <path
                                                d="M7 11V7a5 5 0 0 1 10 0v4"
                                            />
                                        </svg>
                                        <svg
                                            v-else
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
                                            <polyline
                                                points="22 12 18 12 15 21 9 3 6 12 2 12"
                                            />
                                        </svg>
                                    </div>
                                    <div class="income-item__info">
                                        <div class="income-item__name-row">
                                            <span class="income-item__name">{{
                                                income.name
                                            }}</span>
                                            <span
                                                class="income-item__badge"
                                                :class="
                                                    income.type === 'fixed'
                                                        ? 'income-item__badge--fixed'
                                                        : 'income-item__badge--variable'
                                                "
                                            >
                                                {{
                                                    income.type === "fixed"
                                                        ? "Fijo"
                                                        : "Variable"
                                                }}
                                            </span>
                                        </div>
                                        <span
                                            class="income-item__description"
                                            >{{
                                                income.description ||
                                                "Sin descripcion"
                                            }}</span
                                        >
                                    </div>
                                </div>
                                <button
                                    class="income-item__remove"
                                    :disabled="removingIncomeId === income.id"
                                    @click="removeIncome(income)"
                                    :title="`Eliminar ${income.name}`"
                                >
                                    <svg
                                        v-if="removingIncomeId !== income.id"
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
                                        <polyline points="3 6 5 6 21 6" />
                                        <path
                                            d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                                        />
                                    </svg>
                                    <svg
                                        v-else
                                        class="spinner"
                                        xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="2"
                                        width="16"
                                        height="16"
                                    >
                                        <circle
                                            cx="12"
                                            cy="12"
                                            r="10"
                                            stroke-dasharray="30 70"
                                        />
                                    </svg>
                                </button>
                            </div>
                        </TransitionGroup>
                    </div>

                    <!-- Empty State -->
                    <div v-else-if="!showCreateForm" class="empty-state">
                        <div class="empty-state__icon">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="1.5"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                width="36"
                                height="36"
                            >
                                <line x1="12" y1="1" x2="12" y2="23" />
                                <path
                                    d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"
                                />
                            </svg>
                        </div>
                        <p class="empty-state__text">
                            No hay ingresos registrados
                        </p>
                        <p class="empty-state__sub">
                            Crea tu primer ingreso para comenzar
                        </p>
                    </div>

                    <!-- Create Form -->
                    <Transition name="slide">
                        <div v-if="showCreateForm" class="create-form">
                            <div class="create-form__header">
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
                                    <line x1="12" y1="8" x2="12" y2="16" />
                                    <line x1="8" y1="12" x2="16" y2="12" />
                                </svg>
                                <span>Nuevo ingreso</span>
                            </div>

                            <div class="create-form__field">
                                <label class="create-form__label">Nombre</label>
                                <div class="create-form__input-wrapper">
                                    <input
                                        v-model="newIncome.name"
                                        type="text"
                                        class="create-form__input"
                                        placeholder="Ej: Salario, Freelance..."
                                    />
                                </div>
                            </div>

                            <div class="create-form__field">
                                <label class="create-form__label"
                                    >Tipo de ingreso</label
                                >
                                <div class="create-form__type-selector">
                                    <button
                                        type="button"
                                        class="create-form__type-btn"
                                        :class="{
                                            'create-form__type-btn--active':
                                                newIncome.type === 'fixed',
                                        }"
                                        @click="newIncome.type = 'fixed'"
                                    >
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
                                                y="11"
                                                width="18"
                                                height="11"
                                                rx="2"
                                                ry="2"
                                            />
                                            <path
                                                d="M7 11V7a5 5 0 0 1 10 0v4"
                                            />
                                        </svg>
                                        Fijo
                                    </button>
                                    <button
                                        type="button"
                                        class="create-form__type-btn"
                                        :class="{
                                            'create-form__type-btn--active':
                                                newIncome.type === 'variable',
                                        }"
                                        @click="newIncome.type = 'variable'"
                                    >
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
                                            <polyline
                                                points="22 12 18 12 15 21 9 3 6 12 2 12"
                                            />
                                        </svg>
                                        Variable
                                    </button>
                                </div>
                            </div>

                            <div class="create-form__field">
                                <label class="create-form__label"
                                    >Descripcion (opcional)</label
                                >
                                <textarea
                                    v-model="newIncome.description"
                                    class="create-form__textarea"
                                    placeholder="Breve descripcion del ingreso..."
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
                                        isCreating || !newIncome.name.trim()
                                    "
                                    @click="createIncome"
                                >
                                    <svg
                                        v-if="!isCreating"
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
                                        <polyline points="20 6 9 17 4 12" />
                                    </svg>
                                    <svg
                                        v-else
                                        class="spinner"
                                        xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="2"
                                        width="16"
                                        height="16"
                                    >
                                        <circle
                                            cx="12"
                                            cy="12"
                                            r="10"
                                            stroke-dasharray="30 70"
                                        />
                                    </svg>
                                    {{
                                        isCreating
                                            ? "Creando..."
                                            : "Crear ingreso"
                                    }}
                                </button>
                            </div>
                        </div>
                    </Transition>

                    <!-- Create Button -->
                    <button
                        v-if="!showCreateForm"
                        class="create-btn"
                        @click="showCreateForm = true"
                    >
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
                            <line x1="12" y1="8" x2="12" y2="16" />
                            <line x1="8" y1="12" x2="16" y2="12" />
                        </svg>
                        Crear ingreso
                    </button>

                    <!-- Decorative bar -->
                    <div class="panel__accent">
                        <div
                            class="panel__accent-segment panel__accent-segment--green-light"
                        ></div>
                    </div>
                </div>

                <!-- RIGHT PANEL: Income Amounts -->
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
                                <h2 class="panel__title">Monto de ingresos</h2>
                                <p
                                    class="panel__subtitle panel__subtitle--highlight"
                                >
                                    {{ currentMonthYear }}
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Amount Inputs -->
                    <div v-if="incomes.length > 0" class="amounts-section">
                        <div class="amounts-list">
                            <div
                                v-for="income in incomes"
                                :key="income.id"
                                class="amount-row"
                            >
                                <div class="amount-row__label">
                                    <span class="amount-row__name">{{
                                        income.name
                                    }}</span>
                                    <span
                                        class="amount-row__type"
                                        :class="
                                            income.type === 'fixed'
                                                ? 'amount-row__type--fixed'
                                                : 'amount-row__type--variable'
                                        "
                                    >
                                        {{
                                            income.type === "fixed"
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
                                        :value="getAmountForIncome(income.id)"
                                        @input="
                                            (e) =>
                                                setAmountForIncome(
                                                    income.id,
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

                    <!-- No incomes message -->
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
                            Crea tus ingresos primero para poder registrar los
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
                            <h3>Historico de ingresos</h3>
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
/* ===== Layout ===== */
.incomes-view {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 1100px;
    margin: 2.5rem auto;
    padding: 0 1.5rem;
}

.incomes-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
}

@media (min-width: 860px) {
    .incomes-grid {
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
    }
}

/* ===== Blobs ===== */
.blob {
    position: fixed;
    width: 500px;
    height: 500px;
    z-index: 0;
    pointer-events: none;
}
.blob--top-right {
    top: -120px;
    right: -120px;
}
.blob--bottom-left {
    bottom: -150px;
    left: -150px;
}

/* ===== Alerts ===== */
.alert {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.85rem 1.15rem;
    border-radius: 12px;
    font-size: 0.88rem;
    font-weight: 500;
}
.alert--success {
    background: rgba(67, 160, 71, 0.08);
    border: 1px solid rgba(67, 160, 71, 0.2);
    color: var(--primary-color-dark, #388e3c);
}
.alert--error {
    background: rgba(211, 47, 47, 0.06);
    border: 1px solid rgba(211, 47, 47, 0.18);
    color: #c62828;
}
.alert__close {
    margin-left: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border: none;
    background: transparent;
    color: inherit;
    cursor: pointer;
    border-radius: 6px;
    opacity: 0.6;
    transition: opacity 0.15s;
}
.alert__close:hover {
    opacity: 1;
}

.alert-enter-active,
.alert-leave-active {
    transition: all 0.3s ease;
}
.alert-enter-from,
.alert-leave-to {
    opacity: 0;
    transform: translateY(-8px);
}

/* ===== Panel ===== */
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

/* Panel accent bar */
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

/* ===== Income List ===== */
.income-list {
    padding: 0.5rem 0;
}

.income-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.75rem;
    transition:
        background 0.15s,
        opacity 0.3s;
}
.income-item:hover {
    background: rgba(0, 0, 0, 0.015);
}
.income-item--removing {
    opacity: 0.4;
    pointer-events: none;
}

.income-item__left {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    min-width: 0;
}

.income-item__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    min-width: 40px;
    border-radius: 10px;
}
.income-item__icon--fixed {
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color, #43a047);
}
.income-item__icon--variable {
    background: rgba(0, 98, 133, 0.1);
    color: var(--secondary-color, #006285);
}

.income-item__info {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    min-width: 0;
}

.income-item__name-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.income-item__name {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-color, #212121);
}

.income-item__badge {
    padding: 0.12rem 0.5rem;
    border-radius: 5px;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
.income-item__badge--fixed {
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color-dark, #388e3c);
}
.income-item__badge--variable {
    background: rgba(0, 98, 133, 0.1);
    color: var(--secondary-color, #006285);
}

.income-item__description {
    font-size: 0.78rem;
    color: var(--neutral-light, #6b7280);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.income-item__remove {
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
.income-item__remove:hover:not(:disabled) {
    background: rgba(211, 47, 47, 0.08);
    color: #c62828;
}

/* Transitions */
.income-enter-active,
.income-leave-active {
    transition: all 0.3s ease;
}
.income-enter-from {
    opacity: 0;
    transform: translateX(-12px);
}
.income-leave-to {
    opacity: 0;
    transform: translateX(12px);
}

/* ===== Empty State ===== */
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

/* ===== Create Form ===== */
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

/* Type Selector */
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

/* Actions */
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

/* Slide transition */
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

/* ===== Create Button ===== */
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

/* ===== Amounts Section ===== */
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

/* Save button */
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

/* Empty amounts */
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

/* ===== Historical Section ===== */
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

/* Historical empty */
.historical-empty {
    padding: 1.5rem;
    text-align: center;
    color: var(--neutral-light, #6b7280);
    font-size: 0.85rem;
}

/* ===== Skeleton ===== */
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

/* ===== Spinner ===== */
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
