/*
*******************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1B of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*******************************
*/

/*
* Team ID:			[ Team-ID ]
* Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
* Filename:			task_1a.py
* Functions:		readImage, solveMaze
* 					[ Comma separated list of functions in this file ]
* Global variables:	CELL_SIZE
* 					[ List of global variables defined in this file ]
*/


// Include necessary header files
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <arpa/inet.h>


// Constants defined
#define SERVER_PORT 3333
#define RX_BUFFER_SIZE 1024
#define TX_BUFFER_SIZE 1024

#define MAXCHAR 1000				// max characters to read from txt file

// Global variables
struct sockaddr_in dest_addr;
struct sockaddr_in source_addr;

char rx_buffer[RX_BUFFER_SIZE];		// buffer to store data from client
char tx_buffer[RX_BUFFER_SIZE];		// buffer to store data to be sent to client

char ipv4_addr_str[128];			// buffer to store IPv4 addresses as string
char ipv4_addr_str_client[128];		// buffer to store IPv4 addresses as string

int listen_sock;

char line_data[MAXCHAR];
char line_filtered[200],rx_filter[200],d2str[5][10];

FILE *input_fp, *output_fp;

void filter_str(char str[],char filt[])
{
    int i=0,cnt=0;
    while(str[i]!='\0')
    {
        if(str[i]>='0'&&str[i]<='9'||str[i]==','||str[i]==')'||str[i]=='(')
        {
            filt[cnt]=str[i];
            cnt++;  
        }
        i++;
    }  
}

int gt_srch(char str[])
{
    char ch[20];
    int i=0, cnt=0, x=0;
     while(str[i]!='\0')
    {
        if(str[i]=='(')
        {
            for(cnt;str[i]!=')';cnt++,i++)
            {
                d2str[x][cnt]=str[i];
            }
            if(str[i]==')')
            {
                d2str[x][cnt]=str[i];
                x++;
                cnt=0;   
            }   
        }
        i++;
    }
    return x;
}

int cmpre_str(char str[],char search[])
{
    int count1 = 0, count2 = 0, i, j, flag;
    while (str[count1] != '\0')
        count1++;
    while (search[count2] != '\0')
        count2++;
    for (i = 0; i <= count1 - count2; i++)
    {
        for (j = i; j < i + count2; j++)
        {
            flag = 1;
            if (str[j] != search[j - i])
            {
                flag = 0;
                break;
            }
        }
        if (flag == 1)
            break;
    }
    return flag;
}

/*
* Function Name:	socket_create
* Inputs:			dest_addr [ structure type for destination address ]
* 					source_addr [ structure type for source address ]
* Outputs: 			my_sock [ socket value, if connection is properly created ]
* Purpose: 			the function creates the socket connection with the server
* Example call: 	int sock = socket_create(dest_addr, source_addr);
*/

int socket_create(struct sockaddr_in dest_addr, struct sockaddr_in source_addr){

	int addr_family;
	int ip_protocol;

	

    //need to store ipv4 address as string
		
	dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	dest_addr.sin_family = AF_INET;
	dest_addr.sin_port = htons(SERVER_PORT);
	addr_family = AF_INET;
	ip_protocol = IPPROTO_IP;

	listen_sock=socket(addr_family, SOCK_STREAM, ip_protocol);
	if(listen_sock!=-1)
	{
		printf("[DEBUG] Socket created\n");
	}
	else
	{
		printf("sock not created\n");
	}

	if(bind(listen_sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr))==0)
	{
		printf("[DEBUG] Socket bound, port %d\n",SERVER_PORT);
	}
	if(listen(listen_sock, 1)==0)
	{
		printf("[DEBUG] Socket listening\n");
	}

	int my_sock,len;
	len=sizeof(source_addr);
	if((my_sock=accept(listen_sock, (struct sockaddr*)&source_addr, &len))!=-1)
	{
		printf("[DEBUG] Socket accepted\n");
	}

	return my_sock;
}

/*
* Function Name:	receive_from_send_to_client
* Inputs:			sock [ socket value, if connection is properly created ]
* Outputs: 			None
* Purpose: 			the function receives the data from server and updates the 'rx_buffer'
*					variable with it, sends the obstacle position based on obstacle_pos.txt
*					file and sends this information to the client in the provided format.
* Example call: 	receive_from_send_to_client(sock);
*/
int receive_from_send_to_client(int sock){
	bzero(rx_buffer,RX_BUFFER_SIZE);
	recv(sock, rx_buffer, sizeof(rx_buffer),0); 
	printf("From client:%s",rx_buffer);

	int flg=0,len_2d; 
    
    filter_str(line_data,line_filtered);
    filter_str(rx_buffer,rx_filter);
    len_2d=gt_srch(line_filtered);

    for(int i=0;i<len_2d;i++)
    {
        flg=cmpre_str(rx_filter,d2str[i]);
        if(flg==1)
        {
            strcpy(tx_buffer,"@");
            strcat(tx_buffer,d2str[i]);
            strcat(tx_buffer,"@");
			break;
        }
        flg=0;
    }
	send(sock, tx_buffer, sizeof(tx_buffer),0);
	return 0;
}


int main() {
	
    char *input_file_name = "obstacle_pos.txt";
	char *output_file_name = "data_from_client.txt";

	// Create socket and accept connection from client
	int sock = socket_create(dest_addr, source_addr);

	input_fp = fopen(input_file_name, "r");

	if (input_fp == NULL){
		printf("Could not open file %s\n",input_file_name);
		return 1;
	}

	fgets(line_data, MAXCHAR, input_fp);

	output_fp = fopen(output_file_name, "w");

	if (output_fp == NULL){
		printf("Could not open file %s\n",output_file_name);
		return 1;
	}

	while (1) {
		// Receive and send data from client and get the new shortest path
		receive_from_send_to_client(sock);

		// NOTE: YOU ARE NOT ALLOWED TO MAKE ANY CHANGE HERE
		fputs(rx_buffer, output_fp);
		fputs("\n", output_fp);
	}
	return 0;
}
