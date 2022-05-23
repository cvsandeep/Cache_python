import enum


@enum.unique
class Cmd(enum.IntEnum):
    READ_DATA = 0
    WRITE_DATA = 1
    READ_INSTRUCTION = 2
    SNOOPED_INVALIDATE = 3
    SNOOPED_READ = 4
    SNOOPED_WRITE = 5
    SNOOPED_READ_X = 6
    CLEAR_AND_RESET = 8
    PRINT_CACHE_LINE = 9


@enum.unique
class OperationType(enum.IntEnum):
    READ = 1  # Bus Read */
    WRITE = 2  # Bus Write */
    INVALIDATE = 3  # Bus Invalidate */
    RWIM = 4


@enum.unique
class SnoopType(enum.IntEnum):
    NOHIT = 0  # No hit */
    HIT = 1  # Hit */
    HITM = 2  # Hit to modified line */


@enum.unique
class MessageType(enum.IntEnum):
    GETLINE = 1  # Request data for modified line in L1 */
    SENDLINE = 2  # Send requested cache line to L1 */
    INVALIDATELINE = 3  # Invalidate a line in L1 */
    EVICTLINE = 4  # Evict a line from L1 */

@enum.unique
class StateType(enum.IntEnum):
    INVALID = 0
    SHARED = 1
    EXCLUSIVE = 2
    MODEFIED = 3
