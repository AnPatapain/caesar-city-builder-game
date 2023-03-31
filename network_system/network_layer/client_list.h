#ifndef CLIENT_LIST
#define CLIENT_LIST

#include <sys/socket.h>
#include <stdint.h>
#include <stdlib.h>

#include "game_packet_protocol.h"

typedef enum {FALSE = 0, TRUE = 1} bool;

struct client_game
{
    int socket_client;
    uint16_t player_id;
    struct sockaddr sockaddr_client;
    u_int socket_size;
    bool as_init;
    struct client_game* next;
};

typedef struct client_game client_game;


client_game *first_client();
bool id_exist(client_game *client_to_check,uint16_t id);
int cgl_append(client_game* new_client);
game_ip *get_all_ips(int *nb_client);

/**
 * @param: fd_server: fd to set al client
 * @return: Fd max
*/
int cgl_set_all_client(fd_set *fd_server);

#endif //CLIENT_LIST