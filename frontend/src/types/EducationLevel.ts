const EDUCATION_LEVELS = {
    PRIMARY: "Primaria",
    SECONDARY: "Secundaria",
    HIGH_SCHOOL: "Bachillerato",
    BACHELOR: "Licenciatura",
    MASTER: "Maestría",
    DOCTORATE: "Doctorado",
} as const;

type EducationLevel = keyof typeof EDUCATION_LEVELS;

const EDUCATION_LEVEL_OPTIONS = Object.entries(EDUCATION_LEVELS).map(
    ([key, value]) => ({
        content: value,
        value: key as EducationLevel,
    }),
);

export { EDUCATION_LEVELS, EDUCATION_LEVEL_OPTIONS };
export type { EducationLevel };
