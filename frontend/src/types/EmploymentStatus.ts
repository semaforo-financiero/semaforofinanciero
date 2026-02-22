const EMPLOYMENT_STATUSES = {
    EMPLOYED: "Empleado",
    SELF_EMPLOYED: "Independiente",
    STUDENT: "Estudiante",
    UNEMPLOYED: "Desempleado",
    RETIRED: "Jubilado",
    HOMEMAKER: "Ama de casa",
} as const;

type EmploymentStatus = keyof typeof EMPLOYMENT_STATUSES;

const EMPLOYMENT_STATUS_OPTIONS = Object.entries(EMPLOYMENT_STATUSES).map(
    ([key, value]) => ({
        content: value,
        value: key as EmploymentStatus,
    }),
);

export { EMPLOYMENT_STATUSES, EMPLOYMENT_STATUS_OPTIONS };
export type { EmploymentStatus };
