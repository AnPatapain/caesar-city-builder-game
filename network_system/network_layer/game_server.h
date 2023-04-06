#ifndef GAME_SERVER
#define GAME_SERVER

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/un.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>

#include "game_packet_protocol.h"
#include "client_list.h"

/**
 * Timeout for the connection in seconds
 */
#define TIMEOUT 10

#define SYSSOCK "/tmp/socket"

int init_server(const char *ip_address);
int req_connection(client_game *client, const game_packet *packet);
int connection_existant_game(game_ip ip_address, bool is_new_player);

#endif //GAME_SERVER