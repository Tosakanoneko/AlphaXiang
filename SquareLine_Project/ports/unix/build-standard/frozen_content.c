//
// Content for MICROPY_MODULE_FROZEN_STR
//
#include <stdint.h>
const char mp_frozen_str_names[] = {
"\0"};
const uint32_t mp_frozen_str_sizes[] = {
0};
const char mp_frozen_str_content[] = {
"\0"};
//
// Content for MICROPY_MODULE_FROZEN_MPY
//
#include "py/emitglue.h"
extern const qstr_pool_t mp_qstr_const_pool;
const qstr_pool_t mp_qstr_frozen_const_pool = {
    (qstr_pool_t*)&mp_qstr_const_pool, MP_QSTRnumber_of, 0, false, 0
};
const char mp_frozen_mpy_names[1] = {"\0"};
const mp_raw_code_t *const mp_frozen_mpy_content[1] = {NULL};
