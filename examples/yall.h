#include <string.h>

#define MAX 42
#define MIN 0xACDC
#define SERIAL "ARD32HEE"
#define TERM '0'


/**
 * What is this!?
 */
enum bar {
  BAR_FIRST,
  BAR_SECOND = 3
};

enum baz { BAZ_FIRST, BAZ_SECOND = 0x4, BAZ_THIRD = 0x42 };

enum foo {
    FOO_FIRST,
    FOO_SECOND = 2,
    FOO_THIRD = 0x3
};

/**
* This is a structure with variable length members
*/
struct variable_len {
  unsigned long long foo;
  short bar;
  int baz;
};

/**
 * Here is  a comment,
 * it is multiple lines,
 * it is awesome!
 */ 
struct foo {
  i8 ifw8;
  i16 ifw16;
  i32 ifw32;
  i64 ifw64;

  u8 ufw8;
  u16 ufw16;
  u32 ufw32;
  u64 ufw64;
};
