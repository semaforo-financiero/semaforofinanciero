const GENDERS = {
    MALE: "Masculino",
    FEMALE: "Femenino",
} as const;

type Gender = keyof typeof GENDERS;

const GENDER_OPTIONS = Object.entries(GENDERS).map(([key, value]) => ({
    content: value,
    value: key as Gender,
}));

export { GENDERS, GENDER_OPTIONS };
export type { Gender };
