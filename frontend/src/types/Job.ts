const JOBS = {
    TECHNOLOGY: "Tecnología",
    EDUCATION: "Enseñanza",
    HEALTHCARE: "Salud",
    FINANCE: "Finanzas",
    COMMERCE: "Comercio",
    INDUSTRY: "Industria",
    CONSTRUCTION: "Construcción",
    TRANSPORTATION: "Transporte",
    AGRICULTURE: "Agricultura",
    GOVERNMENT: "Gobierno / Sector público",
    POLITICS: "Política",
    LEGAL: "Derecho",
    MARKETING: "Marketing y Publicidad",
    ARTS: "Arte y Cultura",
    MEDIA: "Medios de comunicación",
    TOURISM: "Turismo y Hospitalidad",
    SECURITY: "Seguridad",
    SCIENCE: "Ciencia e Investigación",
    SPORTS: "Deportes",
    OTHER: "Otro",
} as const;

type Job = keyof typeof JOBS;

const JOBS_OPTIONS = Object.entries(JOBS).map(([key, value]) => ({
    content: value,
    value: key as Job,
}));

export { JOBS, JOBS_OPTIONS };
export type { Job };
