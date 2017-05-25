#include "Python.h"

#include <ctype.h>
#include <string.h>

#ifndef HAVE_STRINGS_H
#ifdef _MSC_VER
//not #if defined(_WIN32) || defined(_WIN64) because we have strncasecmp in
//mingw
#undef strncasecmp
#define strncasecmp _strnicmp
#else
#error "define strncasecmp() for non-posix, non-windows?"
#endif /* !_MSC_VER */
#endif /* !HAVE_STRINGS_H */

typedef struct
{
    const char* numeral;
    int value;
    int size;
} Numeral;

/**
 * Convert positive *n* to Roman *numeral*s.
 *
 * *numeral* should be allocated buffer at least *size* size.
 *
 * Return the number of generated Roman numerals or -1 on error.
 */
PyAPI_FUNC(int) Py_to_roman_numerals_from_int(int n, char *numeral, int size)
{
    static const Numeral map[] = {
        {"M",  1000, 1},
        {"CM", 900, 2},
        {"D",  500, 1},
        {"CD", 400, 2},
        {"C",  100, 1},
        {"XC", 90, 2},
        {"L",  50, 1},
        {"XL", 40, 2},
        {"X",  10, 1},
        {"IX", 9, 2},
        {"V",  5, 1},
        {"IV", 4, 2},
        {"I",  1, 1},
    };

    if (n > 3999 || n <= 0)
        return -1; /* out of range */

    int count = 0;
    for (const Numeral *r = map; r != &map[sizeof map / sizeof *map]; ++r) {
        while (n >= r->value) {
            n -= r->value;
            strncpy(numeral + count, r->numeral, r->size);
            count += r->size;
            if (count >= size)
                return -1; /* input buffer is too short */
        }
    }
    return count;
}

static
int roman_numeral_value(unsigned char c)
{
  switch(toupper(c)) {
  case 'I': return 1;
  case 'V': return 5;
  case 'X': return 10;
  case 'L': return 50;
  case 'C': return 100;
  case 'D': return 500;
  case 'M': return 1000;
  default: return 0; // error
  }
}

/** Relaxed version that works on valid Roman numerals but may fail on invalid. */
static int
from_roman(const char *s, int size)
{
  int total = 0, prev = 0;
  for (int i = size-1; i >= 0; --i) { // in reverse order
    int value = roman_numeral_value(s[i]);
    total += value < prev ? -value : value; // subtract if necessary
    prev = value;
  }
  return total;
}

/**
 * Return positive int corresponding to the Roman numeral such as "XIV" given
 * in *ptr.
 *
 * Return negative on error. On return, *ptr points past the last recognized
 * roman numeral.
 */
PyAPI_FUNC(int) Py_from_roman_numerals_to_int(const char **ptr)
{
    char numeral[Py_MAX_ROMAN_SIZE] = {0};
    const char *s = *ptr, *start = s;
    int size = 0;
    for ( ; Py_IS_ROMAN_DIGIT(*s); ++s)
        ++size;
    *ptr = s;
    if (size == 0 || size >= (int)sizeof numeral)
        return -1; /* input is too short or too long */
    int n = from_roman(start, size);
    int ret = Py_to_roman_numerals_from_int(n, numeral, sizeof numeral);
    if (ret < 0 || numeral[size] != '\0' || strncasecmp(start, numeral, size))
        return -1;
    return n;
}
