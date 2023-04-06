#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>

#define C_COMMAND 65535

struct Object_type {
    uint16_t typeObject;
    uint16_t metaData;
};


struct Object_packet {
    struct Object_type object_type;
    uint32_t object_size;
    uint32_t id_object;
    uint16_t id_player;
    uint16_t reserved;
    char *data;
};
typedef struct Object_packet Object_packet;

