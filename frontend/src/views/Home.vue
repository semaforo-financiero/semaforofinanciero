<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/authStore";
import { onMounted, ref, computed, watch } from "vue";

import api from "../lib/api";
import { toasterStore } from "../stores/toasterStore";
import type UserProfile from "../lib/api/models/UserProfile";

import RiskAnalysis from "../lib/api/models/Risk";
import House from "../assets/icons/House.vue";
import Calendar from "../assets/icons/Calendar.vue";
import CurrencySimbol from "../assets/icons/CurrencySimbol.vue";
import Clock from "../assets/icons/Clock.vue";
import Warning from "../assets/icons/Warning.vue";
import InfoCircle from "../assets/icons/InfoCircle.vue";

type ViewMode = "personal" | "family";

const router = useRouter();
const authStore = useAuthStore();
const userProfile = ref<UserProfile | null>(null);
const loadingProfile = ref(false);
const isLoading = ref(true);
const viewMode = ref<ViewMode>("personal");
const analysis = ref<RiskAnalysis | null>(null);

const getProfile = async () => {
    try {
        loadingProfile.value = true;

        const token = authStore.getAccessToken();

        if (!token) {
            throw new Error("No se encontró el token de autenticación");
        }

        userProfile.value = await api.profile.get(token);

        const socioEconomicProfile = userProfile.value.socioeconomic_profile;

        if (
            !socioEconomicProfile ||
            Object.values(socioEconomicProfile).some(
                (value) => value === null || value === undefined,
            )
        ) {
            router.push({ name: "profile" });
        }
    } catch (error) {
        toasterStore.error(
            "Error al cargar el perfil",
            "Por favor inicia sesión nuevamente.",
        );
    } finally {
        loadingProfile.value = false;
    }
};

const riskColor = computed(() => {
    if (!analysis.value) {
        return "#6b7280";
    }

    const colors = {
        HIGH: "#dc2626",
        MEDIUM: "#f59e0b",
        LOW: "#43a047",
    };

    return colors[analysis.value.risk as keyof typeof colors];
});

const riskLabel = computed(() => {
    if (!analysis.value) {
        return "";
    }

    const labels = {
        HIGH: "Alto",
        MEDIUM: "Medio",
        LOW: "Bajo",
    };

    return labels[analysis.value.risk as keyof typeof labels];
});

const scoreRotation = computed(() => {
    if (!analysis.value) {
        return 0;
    }

    return (analysis.value.score / 100) * 180;
});

const highRules = computed(
    () => analysis.value?.rules.filter((r) => r.severity === "HIGH") || [],
);

const mediumRules = computed(
    () => analysis.value?.rules.filter((r) => r.severity === "MEDIUM") || [],
);

const lowRules = computed(
    () => analysis.value?.rules.filter((r) => r.severity === "LOW") || [],
);

const expenseBreakdown = computed(() => {
    if (!analysis.value) {
        return [];
    }

    const ind = analysis.value.indicators;

    return [
        {
            label: "Gastos Fijos",
            value: ind.fixed_expense_amount,
            color: "#006285",
        },
        {
            label: "Gastos Variables",
            value: ind.variable_expense_amount,
            color: "#43a047",
        },
        { label: "Deuda", value: ind.debt_expense_amount, color: "#f59e0b" },
    ];
});

const totalExpenseBreakdown = computed(() => {
    return expenseBreakdown.value
        .slice(0, -1)
        .reduce((sum, item) => sum + item.value, 0);
});

const viewTitle = computed(() => {
    return viewMode.value === "personal"
        ? "Analisis Personal"
        : "Analisis Familiar";
});

const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("es-MX", {
        style: "currency",
        currency: "MXN",
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(value);
};

const formatPercent = (value: number) => {
    return `${(value * 100).toFixed(0)}%`;
};

const getEmploymentLabel = (status: string) => {
    const labels: Record<string, string> = {
        EMPLOYED: "Empleado",
        SELF_EMPLOYED: "Independiente",
        UNEMPLOYED: "Desempleado",
        RETIRED: "Jubilado",
        MIXED: "Mixto",
    };

    return labels[status] || status;
};

const getSeverityBg = (severity: string) => {
    const colors: Record<string, string> = {
        HIGH: "rgba(220, 38, 38, 0.08)",
        MEDIUM: "rgba(245, 158, 11, 0.08)",
        LOW: "rgba(67, 160, 71, 0.08)",
    };

    return (
        colors[severity as keyof typeof colors] || "rgba(107, 114, 128, 0.08)"
    );
};

const fetchAnalysis = async () => {
    isLoading.value = true;
    analysis.value = null;

    try {
        const token = authStore.getAccessToken();

        if (!token) {
            throw new Error("No se encontró el token de autenticación");
        }

        if (viewMode.value === "personal") {
            analysis.value = await api.risk.getByUser(token);
        } else {
            analysis.value = await api.risk.getByFamily(token);
        }

        // await new Promise((resolve) => setTimeout(resolve, 1200));
        // analysis.value =
        //     viewMode.value === "personal" ? mockPersonalData : mockFamilyData;
    } catch (error) {
        toasterStore.error(
            "Error al cargar el riesgo financiero",
            "Por favor intenta de nuevo.",
        );
    } finally {
        isLoading.value = false;
    }
};

watch(viewMode, () => {
    fetchAnalysis();
});

onMounted(() => {
    getProfile();
    fetchAnalysis();
});
</script>

<template>
    <div class="dashboard">
        <header class="dashboard-header">
            <div class="dashboard-header__left">
                <div class="dashboard-header__icon">
                    <House />
                </div>
                <div>
                    <h1 class="dashboard-header__title">Semaforo Financiero</h1>
                    <p class="dashboard-header__subtitle">{{ viewTitle }}</p>
                </div>
            </div>

            <div class="dashboard-header__right">
                <div class="view-toggle">
                    <button
                        class="view-toggle__btn"
                        :class="{
                            'view-toggle__btn--active': viewMode === 'personal',
                        }"
                        @click="viewMode = 'personal'"
                        :disabled="isLoading"
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
                            <path
                                d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"
                            />
                            <circle cx="12" cy="7" r="4" />
                        </svg>
                        <span>Personal</span>
                    </button>
                    <button
                        class="view-toggle__btn"
                        :class="{
                            'view-toggle__btn--active': viewMode === 'family',
                        }"
                        @click="viewMode = 'family'"
                        :disabled="isLoading"
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
                            <path
                                d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"
                            />
                            <circle cx="9" cy="7" r="4" />
                            <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                        </svg>
                        <span>Familiar</span>
                    </button>
                </div>

                <div class="dashboard-header__date">
                    <Calendar />
                    {{
                        new Date().toLocaleDateString("es-MX", {
                            year: "numeric",
                            month: "long",
                            day: "numeric",
                        })
                    }}
                </div>
            </div>
        </header>

        <!-- Loading Skeleton -->
        <template v-if="isLoading">
            <div class="dashboard-grid">
                <div class="card card--skeleton">
                    <div class="skeleton-content skeleton-content--score">
                        <div class="skeleton-gauge">
                            <div class="skeleton skeleton--circle"></div>
                        </div>
                        <div class="skeleton-info">
                            <div class="skeleton skeleton--badge"></div>
                            <div class="skeleton skeleton--text"></div>
                            <div
                                class="skeleton skeleton--text skeleton--short"
                            ></div>
                        </div>
                    </div>
                    <div class="skeleton-scale">
                        <div class="skeleton skeleton--pill"></div>
                        <div class="skeleton skeleton--pill"></div>
                        <div class="skeleton skeleton--pill"></div>
                    </div>
                </div>

                <div class="card card--skeleton">
                    <div class="skeleton-header">
                        <div class="skeleton skeleton--icon"></div>
                        <div class="skeleton skeleton--title"></div>
                    </div>
                    <div class="skeleton-grid">
                        <div class="skeleton skeleton--card"></div>
                        <div class="skeleton skeleton--card"></div>
                        <div class="skeleton skeleton--card"></div>
                        <div class="skeleton skeleton--card"></div>
                    </div>
                    <div class="skeleton-bar-section">
                        <div class="skeleton skeleton--bar-label"></div>
                        <div class="skeleton skeleton--bar"></div>
                    </div>
                </div>

                <div class="card card--skeleton">
                    <div class="skeleton-header">
                        <div class="skeleton skeleton--icon"></div>
                        <div class="skeleton skeleton--title"></div>
                    </div>
                    <div class="skeleton-chart">
                        <div class="skeleton skeleton--donut"></div>
                    </div>
                    <div class="skeleton-legend">
                        <div class="skeleton skeleton--legend-item"></div>
                        <div class="skeleton skeleton--legend-item"></div>
                        <div class="skeleton skeleton--legend-item"></div>
                    </div>
                </div>

                <div class="card card--skeleton">
                    <div class="skeleton-header">
                        <div class="skeleton skeleton--icon"></div>
                        <div class="skeleton skeleton--title"></div>
                    </div>
                    <div class="skeleton-indicators">
                        <div class="skeleton skeleton--indicator"></div>
                        <div class="skeleton skeleton--indicator"></div>
                        <div class="skeleton skeleton--indicator"></div>
                        <div class="skeleton skeleton--indicator"></div>
                    </div>
                </div>

                <div class="card card--skeleton card--wide">
                    <div class="skeleton-header">
                        <div class="skeleton skeleton--icon"></div>
                        <div class="skeleton skeleton--title"></div>
                        <div class="skeleton skeleton--badge-small"></div>
                    </div>
                    <div class="skeleton-alerts">
                        <div class="skeleton skeleton--alert"></div>
                        <div class="skeleton skeleton--alert"></div>
                        <div class="skeleton skeleton--alert"></div>
                    </div>
                </div>

                <div class="card card--skeleton">
                    <div class="skeleton-header">
                        <div class="skeleton skeleton--icon"></div>
                        <div class="skeleton skeleton--title"></div>
                    </div>
                    <div class="skeleton-recommendations">
                        <div class="skeleton skeleton--recommendation"></div>
                        <div class="skeleton skeleton--recommendation"></div>
                        <div class="skeleton skeleton--recommendation"></div>
                    </div>
                </div>
            </div>
        </template>

        <!-- Dashboard Content -->
        <template v-else-if="analysis">
            <div class="dashboard-grid">
                <div class="card card--score">
                    <div class="score-card">
                        <div class="score-gauge">
                            <svg viewBox="0 0 200 120" class="score-gauge__svg">
                                <path
                                    d="M 20 100 A 80 80 0 0 1 180 100"
                                    fill="none"
                                    stroke="#e5e7eb"
                                    stroke-width="16"
                                    stroke-linecap="round"
                                />
                                <path
                                    d="M 20 100 A 80 80 0 0 1 180 100"
                                    fill="none"
                                    :stroke="riskColor"
                                    stroke-width="16"
                                    stroke-linecap="round"
                                    :stroke-dasharray="`${(analysis.score / 100) * 251.2} 251.2`"
                                    class="score-gauge__progress"
                                />
                                <circle cx="100" cy="100" r="50" fill="white" />
                                <text
                                    x="100"
                                    y="95"
                                    text-anchor="middle"
                                    class="score-gauge__value"
                                >
                                    {{ analysis.score }}
                                </text>
                                <text
                                    x="100"
                                    y="112"
                                    text-anchor="middle"
                                    class="score-gauge__label"
                                >
                                    puntos
                                </text>
                            </svg>

                            <div
                                class="score-gauge__needle"
                                :style="{
                                    transform: `rotate(${scoreRotation - 90}deg)`,
                                }"
                            >
                                <div class="score-gauge__needle-inner"></div>
                            </div>
                        </div>

                        <div class="score-info">
                            <div
                                class="score-info__badge"
                                :style="{
                                    backgroundColor: getSeverityBg(
                                        analysis.risk,
                                    ),
                                    color: riskColor,
                                }"
                            >
                                <svg
                                    v-if="analysis.risk === 'HIGH'"
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
                                        d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                                    />
                                    <line x1="12" y1="9" x2="12" y2="13" />
                                    <line x1="12" y1="17" x2="12.01" y2="17" />
                                </svg>
                                <svg
                                    v-else-if="analysis.risk === 'MEDIUM'"
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
                                    <line x1="12" y1="8" x2="12" y2="12" />
                                    <line x1="12" y1="16" x2="12.01" y2="16" />
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
                                    <path
                                        d="M22 11.08V12a10 10 0 1 1-5.93-9.14"
                                    />
                                    <polyline points="22 4 12 14.01 9 11.01" />
                                </svg>
                                Riesgo {{ riskLabel }}
                            </div>
                            <p class="score-info__text">
                                <template v-if="viewMode === 'personal'">
                                    Tu puntuacion personal indica un nivel de
                                    riesgo
                                </template>
                                <template v-else>
                                    La puntuacion familiar indica un nivel de
                                    riesgo
                                </template>
                                <strong :style="{ color: riskColor }">{{
                                    riskLabel.toLowerCase()
                                }}</strong
                                >. Se detectaron
                                <strong
                                    >{{ analysis.rules.length }} alertas</strong
                                >
                                en el perfil financiero.
                            </p>
                        </div>
                    </div>

                    <div class="score-scale">
                        <div class="score-scale__item score-scale__item--low">
                            <span class="score-scale__dot"></span>
                            <span>0-29 Bajo</span>
                        </div>
                        <div
                            class="score-scale__item score-scale__item--medium"
                        >
                            <span class="score-scale__dot"></span>
                            <span>30-59 Medio</span>
                        </div>
                        <div class="score-scale__item score-scale__item--high">
                            <span class="score-scale__dot"></span>
                            <span>+60 Alto</span>
                        </div>
                    </div>
                </div>

                <div class="card card--summary">
                    <div class="card__header">
                        <CurrencySimbol />
                        <h2>Resumen Financiero</h2>
                        <span
                            class="card__header-scope"
                            :class="
                                viewMode === 'family'
                                    ? 'card__header-scope--family'
                                    : ''
                            "
                        >
                            {{
                                viewMode === "personal"
                                    ? "Personal"
                                    : "Familiar"
                            }}
                        </span>
                    </div>

                    <div class="summary-grid">
                        <div class="summary-item summary-item--income">
                            <div class="summary-item__icon">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    width="20"
                                    height="20"
                                >
                                    <polyline
                                        points="23 6 13.5 15.5 8.5 10.5 1 18"
                                    />
                                    <polyline points="17 6 23 6 23 12" />
                                </svg>
                            </div>
                            <div class="summary-item__content">
                                <span class="summary-item__label"
                                    >Ingresos</span
                                >
                                <span class="summary-item__value">{{
                                    formatCurrency(analysis.indicators.income)
                                }}</span>
                            </div>
                        </div>

                        <div class="summary-item summary-item--expense">
                            <div class="summary-item__icon">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    width="20"
                                    height="20"
                                >
                                    <polyline
                                        points="23 18 13.5 8.5 8.5 13.5 1 6"
                                    />
                                    <polyline points="17 18 23 18 23 12" />
                                </svg>
                            </div>
                            <div class="summary-item__content">
                                <span class="summary-item__label">Egresos</span>
                                <span class="summary-item__value">{{
                                    formatCurrency(analysis.indicators.expense)
                                }}</span>
                            </div>
                        </div>

                        <div
                            class="summary-item"
                            :class="
                                analysis.indicators.savings >= 0
                                    ? 'summary-item--positive'
                                    : 'summary-item--negative'
                            "
                        >
                            <div class="summary-item__icon">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    width="20"
                                    height="20"
                                >
                                    <path
                                        d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"
                                    />
                                </svg>
                            </div>
                            <div class="summary-item__content">
                                <span class="summary-item__label">Ahorro</span>
                                <span class="summary-item__value">{{
                                    formatCurrency(analysis.indicators.savings)
                                }}</span>
                            </div>
                        </div>

                        <div class="summary-item summary-item--neutral">
                            <div class="summary-item__icon">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    width="20"
                                    height="20"
                                >
                                    <rect
                                        x="1"
                                        y="4"
                                        width="22"
                                        height="16"
                                        rx="2"
                                        ry="2"
                                    />
                                    <line x1="1" y1="10" x2="23" y2="10" />
                                </svg>
                            </div>
                            <div class="summary-item__content">
                                <span class="summary-item__label"
                                    >Deuda mensual</span
                                >
                                <span class="summary-item__value">{{
                                    formatCurrency(
                                        analysis.indicators.debt_expense_amount,
                                    )
                                }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="comparison-bar">
                        <div class="comparison-bar__header">
                            <span>Ingresos vs Egresos</span>
                            <span
                                class="comparison-bar__ratio"
                                :class="
                                    analysis.indicators.expense_ratio > 1
                                        ? 'comparison-bar__ratio--danger'
                                        : 'comparison-bar__ratio--success'
                                "
                            >
                                {{
                                    formatPercent(
                                        analysis.indicators.expense_ratio,
                                    )
                                }}
                                de los ingresos
                            </span>
                        </div>
                        <div class="comparison-bar__track">
                            <div
                                class="comparison-bar__fill comparison-bar__fill--income"
                                :style="{ width: '100%' }"
                            ></div>
                            <div
                                class="comparison-bar__fill comparison-bar__fill--expense"
                                :style="{
                                    width: `${Math.min(analysis.indicators.expense_ratio * 100, 100)}%`,
                                }"
                            ></div>
                        </div>
                        <div class="comparison-bar__legend">
                            <span class="comparison-bar__legend-item">
                                <span
                                    class="comparison-bar__legend-dot comparison-bar__legend-dot--income"
                                ></span>
                                Ingresos
                            </span>
                            <span class="comparison-bar__legend-item">
                                <span
                                    class="comparison-bar__legend-dot comparison-bar__legend-dot--expense"
                                ></span>
                                Egresos
                            </span>
                        </div>
                    </div>
                </div>

                <div class="card card--chart">
                    <div class="card__header">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            width="20"
                            height="20"
                        >
                            <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
                            <path d="M22 12A10 10 0 0 0 12 2v10z" />
                        </svg>
                        <h2>Distribucion de Egresos</h2>
                    </div>

                    <div class="donut-chart">
                        <svg viewBox="0 0 200 200" class="donut-chart__svg">
                            <circle
                                v-for="(item, index) in expenseBreakdown"
                                :key="item.label"
                                cx="100"
                                cy="100"
                                r="70"
                                fill="none"
                                :stroke="item.color"
                                stroke-width="30"
                                :stroke-dasharray="`${(item.value / totalExpenseBreakdown) * 439.8} 439.8`"
                                :stroke-dashoffset="
                                    -expenseBreakdown
                                        .slice(0, index)
                                        .reduce(
                                            (sum, i) =>
                                                sum +
                                                (i.value /
                                                    totalExpenseBreakdown) *
                                                    439.8,
                                            0,
                                        )
                                "
                                class="donut-chart__segment"
                            />
                            <text
                                x="100"
                                y="95"
                                text-anchor="middle"
                                class="donut-chart__total-label"
                            >
                                Total
                            </text>
                            <text
                                x="100"
                                y="115"
                                text-anchor="middle"
                                class="donut-chart__total-value"
                            >
                                {{ formatCurrency(totalExpenseBreakdown) }}
                            </text>
                        </svg>
                    </div>

                    <div class="donut-legend">
                        <div
                            v-for="item in expenseBreakdown"
                            :key="item.label"
                            class="donut-legend__item"
                        >
                            <span
                                class="donut-legend__dot"
                                :style="{ backgroundColor: item.color }"
                            ></span>
                            <span class="donut-legend__label">{{
                                item.label
                            }}</span>
                            <span class="donut-legend__value">{{
                                formatCurrency(item.value)
                            }}</span>
                            <span class="donut-legend__percent">{{
                                formatPercent(
                                    item.value / totalExpenseBreakdown,
                                )
                            }}</span>
                        </div>
                    </div>
                </div>

                <div class="card card--indicators">
                    <div class="card__header">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            width="20"
                            height="20"
                        >
                            <polyline
                                points="22 12 18 12 15 21 9 3 6 12 2 12"
                            />
                        </svg>
                        <h2>Indicadores Clave</h2>
                    </div>

                    <div class="indicators-grid">
                        <div class="indicator-item">
                            <div class="indicator-item__header">
                                <span class="indicator-item__label"
                                    >Ratio de Gastos</span
                                >
                                <span
                                    class="indicator-item__badge"
                                    :class="
                                        analysis.indicators.expense_ratio > 1
                                            ? 'indicator-item__badge--danger'
                                            : 'indicator-item__badge--success'
                                    "
                                >
                                    {{
                                        analysis.indicators.expense_ratio > 1
                                            ? "Excedido"
                                            : "Normal"
                                    }}
                                </span>
                            </div>
                            <div class="indicator-item__value">
                                {{
                                    formatPercent(
                                        analysis.indicators.expense_ratio,
                                    )
                                }}
                            </div>
                            <div class="indicator-item__bar">
                                <div
                                    class="indicator-item__bar-fill"
                                    :class="
                                        analysis.indicators.expense_ratio > 1
                                            ? 'indicator-item__bar-fill--danger'
                                            : 'indicator-item__bar-fill--success'
                                    "
                                    :style="{
                                        width: `${Math.min(analysis.indicators.expense_ratio * 100, 100)}%`,
                                    }"
                                ></div>
                            </div>
                        </div>

                        <div class="indicator-item">
                            <div class="indicator-item__header">
                                <span class="indicator-item__label"
                                    >Ratio de Deuda</span
                                >
                                <span
                                    class="indicator-item__badge"
                                    :class="
                                        analysis.indicators.debt_ratio > 0.4
                                            ? 'indicator-item__badge--danger'
                                            : analysis.indicators.debt_ratio >
                                                0.25
                                              ? 'indicator-item__badge--warning'
                                              : 'indicator-item__badge--success'
                                    "
                                >
                                    {{
                                        analysis.indicators.debt_ratio > 0.4
                                            ? "Alto"
                                            : analysis.indicators.debt_ratio >
                                                0.25
                                              ? "Moderado"
                                              : "Saludable"
                                    }}
                                </span>
                            </div>
                            <div class="indicator-item__value">
                                {{
                                    formatPercent(
                                        analysis.indicators.debt_ratio,
                                    )
                                }}
                            </div>
                            <div class="indicator-item__bar">
                                <div
                                    class="indicator-item__bar-fill"
                                    :class="
                                        analysis.indicators.debt_ratio > 0.4
                                            ? 'indicator-item__bar-fill--danger'
                                            : analysis.indicators.debt_ratio >
                                                0.25
                                              ? 'indicator-item__bar-fill--warning'
                                              : 'indicator-item__bar-fill--success'
                                    "
                                    :style="{
                                        width: `${analysis.indicators.debt_ratio * 100}%`,
                                    }"
                                ></div>
                            </div>
                        </div>

                        <div class="indicator-item">
                            <div class="indicator-item__header">
                                <span class="indicator-item__label"
                                    >Ratio de Ahorro</span
                                >
                                <span
                                    class="indicator-item__badge"
                                    :class="
                                        analysis.indicators.savings_ratio < 0
                                            ? 'indicator-item__badge--danger'
                                            : analysis.indicators
                                                    .savings_ratio < 0.1
                                              ? 'indicator-item__badge--warning'
                                              : 'indicator-item__badge--success'
                                    "
                                >
                                    {{
                                        analysis.indicators.savings_ratio < 0
                                            ? "Negativo"
                                            : analysis.indicators
                                                    .savings_ratio < 0.1
                                              ? "Bajo"
                                              : "Bueno"
                                    }}
                                </span>
                            </div>
                            <div class="indicator-item__value">
                                {{
                                    formatPercent(
                                        analysis.indicators.savings_ratio,
                                    )
                                }}
                            </div>
                            <div class="indicator-item__bar">
                                <div
                                    class="indicator-item__bar-fill"
                                    :class="
                                        analysis.indicators.savings_ratio < 0
                                            ? 'indicator-item__bar-fill--danger'
                                            : analysis.indicators
                                                    .savings_ratio < 0.1
                                              ? 'indicator-item__bar-fill--warning'
                                              : 'indicator-item__bar-fill--success'
                                    "
                                    :style="{
                                        width: `${Math.max(analysis.indicators.savings_ratio * 100 + 50, 0)}%`,
                                    }"
                                ></div>
                            </div>
                        </div>

                        <div class="indicator-item">
                            <div class="indicator-item__header">
                                <span class="indicator-item__label"
                                    >Gastos Variables</span
                                >
                                <span
                                    class="indicator-item__badge"
                                    :class="
                                        analysis.indicators
                                            .variable_expense_ratio > 0.6
                                            ? 'indicator-item__badge--warning'
                                            : 'indicator-item__badge--success'
                                    "
                                >
                                    {{
                                        analysis.indicators
                                            .variable_expense_ratio > 0.6
                                            ? "Alto"
                                            : "Normal"
                                    }}
                                </span>
                            </div>
                            <div class="indicator-item__value">
                                {{
                                    formatPercent(
                                        analysis.indicators
                                            .variable_expense_ratio,
                                    )
                                }}
                            </div>
                            <div class="indicator-item__bar">
                                <div
                                    class="indicator-item__bar-fill"
                                    :class="
                                        analysis.indicators
                                            .variable_expense_ratio > 0.6
                                            ? 'indicator-item__bar-fill--warning'
                                            : 'indicator-item__bar-fill--success'
                                    "
                                    :style="{
                                        width: `${analysis.indicators.variable_expense_ratio * 100}%`,
                                    }"
                                ></div>
                            </div>
                        </div>
                    </div>

                    <div class="profile-info">
                        <div class="profile-info__item">
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
                                    x="2"
                                    y="7"
                                    width="20"
                                    height="14"
                                    rx="2"
                                    ry="2"
                                />
                                <path
                                    d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"
                                />
                            </svg>
                            <span>{{
                                getEmploymentLabel(
                                    analysis.indicators.employment_status,
                                )
                            }}</span>
                        </div>
                        <div class="profile-info__item">
                            <Clock />
                            <span
                                >{{ analysis.indicators.years_working }} años de
                                experiencia</span
                            >
                        </div>
                        <div class="profile-info__item">
                            <Calendar />
                            <span
                                >{{ analysis.indicators.months_analyzed }} meses
                                analizados</span
                            >
                        </div>
                    </div>
                </div>

                <div class="card card--alerts">
                    <div class="card__header">
                        <Warning />
                        <h2>Alertas Detectadas</h2>
                        <span class="card__header-badge">{{
                            analysis.rules.length
                        }}</span>
                    </div>

                    <div class="alerts-list">
                        <template v-if="highRules.length > 0">
                            <div class="alerts-group">
                                <div
                                    class="alerts-group__header alerts-group__header--high"
                                >
                                    <span class="alerts-group__dot"></span>
                                    Severidad Alta ({{ highRules.length }})
                                </div>
                                <div
                                    v-for="rule in highRules"
                                    :key="rule.code"
                                    class="alert-item alert-item--high"
                                >
                                    <div class="alert-item__icon">
                                        <Warning />
                                    </div>
                                    <div class="alert-item__content">
                                        <p class="alert-item__message">
                                            {{ rule.message }}
                                        </p>
                                        <p class="alert-item__recommendation">
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
                                                <circle
                                                    cx="12"
                                                    cy="12"
                                                    r="10"
                                                />
                                                <path
                                                    d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"
                                                />
                                                <line
                                                    x1="12"
                                                    y1="17"
                                                    x2="12.01"
                                                    y2="17"
                                                />
                                            </svg>
                                            {{ rule.recommendation }}
                                        </p>
                                    </div>
                                    <div class="alert-item__score">
                                        +{{ rule.score }}
                                    </div>
                                </div>
                            </div>
                        </template>

                        <!-- Medium severity -->
                        <template v-if="mediumRules.length > 0">
                            <div class="alerts-group">
                                <div
                                    class="alerts-group__header alerts-group__header--medium"
                                >
                                    <span class="alerts-group__dot"></span>
                                    Severidad Media ({{ mediumRules.length }})
                                </div>
                                <div
                                    v-for="rule in mediumRules"
                                    :key="rule.code"
                                    class="alert-item alert-item--medium"
                                >
                                    <div class="alert-item__icon">
                                        <InfoCircle />
                                    </div>
                                    <div class="alert-item__content">
                                        <p class="alert-item__message">
                                            {{ rule.message }}
                                        </p>
                                        <p class="alert-item__recommendation">
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
                                                <circle
                                                    cx="12"
                                                    cy="12"
                                                    r="10"
                                                />
                                                <path
                                                    d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"
                                                />
                                                <line
                                                    x1="12"
                                                    y1="17"
                                                    x2="12.01"
                                                    y2="17"
                                                />
                                            </svg>
                                            {{ rule.recommendation }}
                                        </p>
                                    </div>
                                    <div class="alert-item__score">
                                        +{{ rule.score }}
                                    </div>
                                </div>
                            </div>
                        </template>

                        <template v-if="lowRules.length > 0">
                            <div class="alerts-group">
                                <div
                                    class="alerts-group__header alerts-group__header--low"
                                >
                                    <span class="alerts-group__dot"></span>
                                    Severidad Baja ({{ lowRules.length }})
                                </div>
                                <div
                                    v-for="rule in lowRules"
                                    :key="rule.code"
                                    class="alert-item alert-item--low"
                                >
                                    <div class="alert-item__icon">
                                        <InfoCircle />
                                    </div>
                                    <div class="alert-item__content">
                                        <p class="alert-item__message">
                                            {{ rule.message }}
                                        </p>
                                        <p class="alert-item__recommendation">
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
                                                <circle
                                                    cx="12"
                                                    cy="12"
                                                    r="10"
                                                />
                                                <path
                                                    d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"
                                                />
                                                <line
                                                    x1="12"
                                                    y1="17"
                                                    x2="12.01"
                                                    y2="17"
                                                />
                                            </svg>
                                            {{ rule.recommendation }}
                                        </p>
                                    </div>
                                    <div class="alert-item__score">
                                        +{{ rule.score }}
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>

                <div class="card card--recommendations">
                    <div class="card__header">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            width="20"
                            height="20"
                        >
                            <circle cx="12" cy="12" r="10" />
                            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
                            <line x1="12" y1="17" x2="12.01" y2="17" />
                        </svg>
                        <h2>Recomendaciones</h2>
                    </div>

                    <div class="recommendations-list">
                        <div
                            v-for="(rec, index) in analysis.recommendations"
                            :key="index"
                            class="recommendation-item"
                        >
                            <div class="recommendation-item__number">
                                {{ index + 1 }}
                            </div>
                            <p class="recommendation-item__text">{{ rec }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<style scoped>
.dashboard {
    position: relative;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1.5rem 3rem;
    min-height: 100vh;
}
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

.dashboard-header {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}
.dashboard-header__left {
    display: flex;
    align-items: center;
    gap: 1rem;
}
.dashboard-header__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    border-radius: 14px;
    background: linear-gradient(
        135deg,
        var(--primary-color, #43a047),
        var(--primary-color-light, #66bb6a)
    );
    color: white;
    box-shadow: 0 4px 12px rgba(67, 160, 71, 0.3);
}
.dashboard-header__title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-color, #212121);
}
.dashboard-header__subtitle {
    font-size: 0.88rem;
    color: var(--neutral-light, #6b7280);
    margin-top: 0.15rem;
}
.dashboard-header__right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.75rem;
}
.dashboard-header__date {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.82rem;
    color: var(--neutral-light, #6b7280);
}

.view-toggle {
    display: flex;
    background: #f3f4f6;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.view-toggle__btn {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 9px;
    background: transparent;
    color: var(--neutral-light, #6b7280);
    font-size: 0.85rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s ease;
}
.view-toggle__btn:hover:not(:disabled) {
    color: var(--text-color, #212121);
}
.view-toggle__btn--active {
    background: white;
    color: var(--primary-color, #43a047);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.view-toggle__btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
.view-toggle__btn span {
    display: none;
}
@media (min-width: 480px) {
    .view-toggle__btn span {
        display: inline;
    }
}

.dashboard-grid {
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
}
@media (min-width: 768px) {
    .dashboard-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
@media (min-width: 1024px) {
    .dashboard-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .card--alerts,
    .card--wide {
        grid-column: span 2;
    }
}

.card {
    background: white;
    border-radius: 20px;
    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.06),
        0 8px 24px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.04);
    overflow: hidden;
}
.card__header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    color: var(--text-color, #212121);
}
.card__header h2 {
    font-size: 1rem;
    font-weight: 700;
}
.card__header-badge {
    margin-left: auto;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    background: rgba(220, 38, 38, 0.1);
    color: #dc2626;
    font-size: 0.75rem;
    font-weight: 700;
}
.card__header-scope {
    margin-left: auto;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color-dark, #388e3c);
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
.card__header-scope--family {
    background: rgba(0, 98, 133, 0.1);
    color: var(--secondary-color, #006285);
}

.card--skeleton {
    padding: 1.5rem;
}

.skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
    border-radius: 8px;
}

@keyframes shimmer {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}

.skeleton-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}
.skeleton--icon {
    width: 24px;
    height: 24px;
    border-radius: 6px;
}
.skeleton--title {
    width: 140px;
    height: 20px;
}
.skeleton--badge-small {
    width: 32px;
    height: 24px;
    margin-left: auto;
    border-radius: 6px;
}

.skeleton-content--score {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}
@media (min-width: 480px) {
    .skeleton-content--score {
        flex-direction: row;
        align-items: flex-start;
    }
}
.skeleton-gauge {
    width: 180px;
    height: 110px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.skeleton--circle {
    width: 160px;
    height: 80px;
    border-radius: 80px 80px 0 0;
}
.skeleton-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}
.skeleton--badge {
    width: 120px;
    height: 36px;
    border-radius: 10px;
}
.skeleton--text {
    width: 100%;
    height: 16px;
}
.skeleton--short {
    width: 70%;
}
.skeleton-scale {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
}
.skeleton--pill {
    width: 80px;
    height: 20px;
    border-radius: 10px;
}
.skeleton-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
}
.skeleton--card {
    height: 80px;
    border-radius: 14px;
}

.skeleton-bar-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
.skeleton--bar-label {
    width: 50%;
    height: 14px;
}
.skeleton--bar {
    width: 100%;
    height: 12px;
    border-radius: 6px;
}
.skeleton-chart {
    display: flex;
    justify-content: center;
    padding: 1rem;
}
.skeleton--donut {
    width: 160px;
    height: 160px;
    border-radius: 50%;
}
.skeleton-legend {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
}
.skeleton--legend-item {
    width: 100%;
    height: 24px;
    border-radius: 6px;
}

.skeleton-indicators {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}
@media (max-width: 480px) {
    .skeleton-indicators {
        grid-template-columns: 1fr;
    }
}
.skeleton--indicator {
    height: 90px;
    border-radius: 12px;
}
.skeleton-alerts {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}
.skeleton--alert {
    height: 80px;
    border-radius: 12px;
}

.skeleton-recommendations {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}
.skeleton--recommendation {
    height: 60px;
    border-radius: 12px;
}

.card--score {
    padding: 1.5rem;
}
.score-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}
@media (min-width: 480px) {
    .score-card {
        flex-direction: row;
        align-items: flex-start;
    }
}

.score-gauge {
    position: relative;
    width: 180px;
    height: 110px;
    flex-shrink: 0;
}
.score-gauge__svg {
    width: 100%;
    height: 100%;
}
.score-gauge__progress {
    transition: stroke-dasharray 1s ease-out;
}
.score-gauge__value {
    font-size: 32px;
    font-weight: 800;
    fill: var(--text-color, #212121);
}
.score-gauge__label {
    font-size: 12px;
    fill: var(--neutral-light, #6b7280);
}
.score-gauge__needle {
    position: absolute;
    bottom: 10px;
    left: 50%;
    width: 4px;
    height: 60px;
    transform-origin: bottom center;
    transition: transform 1s ease-out;
}
.score-gauge__needle-inner {
    width: 100%;
    height: 100%;
    background: linear-gradient(
        to top,
        var(--text-color, #212121) 0%,
        transparent 100%
    );
    border-radius: 2px;
}

.score-info {
    flex: 1;
}
.score-info__badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
}
.score-info__text {
    font-size: 0.9rem;
    line-height: 1.6;
    color: var(--neutral-light, #6b7280);
}
.score-info__text strong {
    font-weight: 600;
}

.score-scale {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1.25rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
}
.score-scale__item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    color: var(--neutral-light, #6b7280);
}
.score-scale__dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}
.score-scale__item--low .score-scale__dot {
    background: #43a047;
}
.score-scale__item--medium .score-scale__dot {
    background: #f59e0b;
}
.score-scale__item--high .score-scale__dot {
    background: #dc2626;
}

.card--summary {
    padding-bottom: 1.5rem;
}
.summary-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    padding: 1.25rem 1.5rem;
}
.summary-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    border-radius: 14px;
    background: #f9fafb;
}
.summary-item__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 10px;
}
.summary-item--income .summary-item__icon {
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color, #43a047);
}
.summary-item--expense .summary-item__icon {
    background: rgba(220, 38, 38, 0.1);
    color: #dc2626;
}
.summary-item--positive .summary-item__icon {
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color, #43a047);
}
.summary-item--negative .summary-item__icon {
    background: rgba(220, 38, 38, 0.1);
    color: #dc2626;
}
.summary-item--neutral .summary-item__icon {
    background: rgba(0, 98, 133, 0.1);
    color: var(--secondary-color, #006285);
}
.summary-item__content {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}
.summary-item__label {
    font-size: 0.78rem;
    color: var(--neutral-light, #6b7280);
}
.summary-item__value {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-color, #212121);
}

.comparison-bar {
    padding: 0 1.5rem;
}
.comparison-bar__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
    color: var(--neutral-light, #6b7280);
}
.comparison-bar__ratio {
    font-weight: 600;
}
.comparison-bar__ratio--danger {
    color: #dc2626;
}
.comparison-bar__ratio--success {
    color: var(--primary-color, #43a047);
}
.comparison-bar__track {
    position: relative;
    height: 12px;
    border-radius: 6px;
    overflow: hidden;
    background: #e5e7eb;
}
.comparison-bar__fill {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    border-radius: 6px;
    transition: width 1s ease-out;
}
.comparison-bar__fill--income {
    background: var(--primary-color, #43a047);
    z-index: 1;
}
.comparison-bar__fill--expense {
    background: #dc2626;
    z-index: 2;
}
.comparison-bar__legend {
    display: flex;
    gap: 1.5rem;
    margin-top: 0.5rem;
}
.comparison-bar__legend-item {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.75rem;
    color: var(--neutral-light, #6b7280);
}
.comparison-bar__legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}
.comparison-bar__legend-dot--income {
    background: var(--primary-color, #43a047);
}
.comparison-bar__legend-dot--expense {
    background: #dc2626;
}

.card--chart {
    padding-bottom: 1.5rem;
}
.donut-chart {
    display: flex;
    justify-content: center;
    padding: 1rem;
}
.donut-chart__svg {
    width: 180px;
    height: 180px;
    transform: rotate(-90deg);
}
.donut-chart__segment {
    transition: stroke-dasharray 1s ease-out;
}
.donut-chart__total-label {
    font-size: 12px;
    fill: var(--neutral-light, #6b7280);
    transform: rotate(90deg);
    transform-origin: center;
}
.donut-chart__total-value {
    font-size: 14px;
    font-weight: 700;
    fill: var(--text-color, #212121);
    transform: rotate(90deg);
    transform-origin: center;
}
.donut-legend {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    padding: 0 1.5rem;
}
.donut-legend__item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.85rem;
}
.donut-legend__dot {
    width: 12px;
    height: 12px;
    border-radius: 4px;
    flex-shrink: 0;
}
.donut-legend__label {
    flex: 1;
    color: var(--text-color, #212121);
}
.donut-legend__value {
    font-weight: 600;
    color: var(--text-color, #212121);
}
.donut-legend__percent {
    color: var(--neutral-light, #6b7280);
    font-size: 0.78rem;
    min-width: 36px;
    text-align: right;
}

.card--indicators {
    padding-bottom: 1.5rem;
}
.indicators-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    padding: 1.25rem 1.5rem;
}
@media (max-width: 480px) {
    .indicators-grid {
        grid-template-columns: 1fr;
    }
}
.indicator-item {
    padding: 1rem;
    border-radius: 12px;
    background: #f9fafb;
}
.indicator-item__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}
.indicator-item__label {
    font-size: 0.78rem;
    color: var(--neutral-light, #6b7280);
}
.indicator-item__badge {
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
}
.indicator-item__badge--success {
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color-dark, #388e3c);
}
.indicator-item__badge--warning {
    background: rgba(245, 158, 11, 0.1);
    color: #d97706;
}
.indicator-item__badge--danger {
    background: rgba(220, 38, 38, 0.1);
    color: #dc2626;
}
.indicator-item__value {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-color, #212121);
    margin-bottom: 0.5rem;
}
.indicator-item__bar {
    height: 6px;
    border-radius: 3px;
    background: #e5e7eb;
    overflow: hidden;
}
.indicator-item__bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 1s ease-out;
}
.indicator-item__bar-fill--success {
    background: var(--primary-color, #43a047);
}
.indicator-item__bar-fill--warning {
    background: #f59e0b;
}
.indicator-item__bar-fill--danger {
    background: #dc2626;
}

.profile-info {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1rem 1.5rem;
    margin: 0 1.5rem;
    border-radius: 12px;
    background: rgba(0, 98, 133, 0.04);
}
.profile-info__item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.82rem;
    color: var(--secondary-color, #006285);
}

.card--alerts {
    padding-bottom: 1.5rem;
}
.alerts-list {
    padding: 1rem 1.5rem;
}
.alerts-group {
    margin-bottom: 1.25rem;
}
.alerts-group:last-child {
    margin-bottom: 0;
}
.alerts-group__header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.82rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px dashed rgba(0, 0, 0, 0.08);
}
.alerts-group__dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}
.alerts-group__header--high {
    color: #dc2626;
}
.alerts-group__header--high .alerts-group__dot {
    background: #dc2626;
}
.alerts-group__header--medium {
    color: #d97706;
}
.alerts-group__header--medium .alerts-group__dot {
    background: #f59e0b;
}
.alerts-group__header--low {
    color: var(--primary-color-dark, #388e3c);
}
.alerts-group__header--low .alerts-group__dot {
    background: var(--primary-color, #43a047);
}

.alert-item {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 0.6rem;
}
.alert-item:last-child {
    margin-bottom: 0;
}
.alert-item--high {
    background: rgba(220, 38, 38, 0.04);
    border-left: 3px solid #dc2626;
}
.alert-item--medium {
    background: rgba(245, 158, 11, 0.04);
    border-left: 3px solid #f59e0b;
}
.alert-item--low {
    background: rgba(67, 160, 71, 0.04);
    border-left: 3px solid var(--primary-color, #43a047);
}
.alert-item__icon {
    flex-shrink: 0;
    margin-top: 0.1rem;
}
.alert-item--high .alert-item__icon {
    color: #dc2626;
}
.alert-item--medium .alert-item__icon {
    color: #f59e0b;
}
.alert-item--low .alert-item__icon {
    color: var(--primary-color, #43a047);
}
.alert-item__content {
    flex: 1;
    min-width: 0;
}
.alert-item__message {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-color, #212121);
    margin-bottom: 0.35rem;
    line-height: 1.4;
}
.alert-item__recommendation {
    display: flex;
    align-items: flex-start;
    gap: 0.35rem;
    font-size: 0.8rem;
    color: var(--neutral-light, #6b7280);
    line-height: 1.45;
}
.alert-item__recommendation svg {
    flex-shrink: 0;
    margin-top: 0.15rem;
}
.alert-item__score {
    flex-shrink: 0;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    background: rgba(0, 0, 0, 0.06);
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-color, #212121);
}

.card--recommendations {
    padding-bottom: 1.5rem;
}
.recommendations-list {
    padding: 1rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}
.recommendation-item {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    padding: 1rem;
    border-radius: 12px;
    background: rgba(67, 160, 71, 0.04);
    border: 1px solid rgba(67, 160, 71, 0.1);
}
.recommendation-item__number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 8px;
    background: var(--primary-color, #43a047);
    color: white;
    font-size: 0.82rem;
    font-weight: 700;
    flex-shrink: 0;
}
.recommendation-item__text {
    font-size: 0.88rem;
    line-height: 1.5;
    color: var(--text-color, #212121);
}
</style>
