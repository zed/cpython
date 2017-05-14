#ifndef Py_ROMAN_H
#define Py_ROMAN_H
#ifndef Py_LIMITED_API
#ifdef __cplusplus
extern "C" {
#endif

#define Py_MAX_ROMAN_SIZE 16 /* 15 + '\0' */
#define Py_IS_ROMAN_DIGIT(c) (c == 'I' || c == 'V' || c == 'X' || c == 'L' \
            || c == 'i' || c == 'v' || c == 'x' || c == 'l'                \
            || c == 'C' || c == 'D' || c == 'M'                            \
            || c == 'c' || c == 'd' || c == 'm')

PyAPI_FUNC(int) Py_to_roman_numerals_from_int(int n, char *numeral, int size);
PyAPI_FUNC(int) Py_from_roman_numerals_to_int(const char **);

#ifdef __cplusplus
}
#endif
#endif /* !Py_LIMITED_API */
#endif /* !Py_ROMAN_H */
