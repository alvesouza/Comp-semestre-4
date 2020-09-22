package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strconv"
	"time"
)

//Variáveis globais interessantes para o processo
var err string
var myPort string          //porta do meu servidor
var nServers int           //qtde de outros processo
var CliConn []*net.UDPConn //vetor com conexões para os servidores
//dos outros processos
var ServConn *net.UDPConn //conexão do meu servidor (onde recebo
//mensagens dos outros processos)

func CheckError(err error) {
	if err != nil {
		fmt.Println("Erro: ", err)
		os.Exit(0)
	}
}
func PrintError(err error) {
	if err != nil {
		fmt.Println("Erro: ", err)
	}
}
func doServerJob() {
	buf := make([]byte, 1024)

	for {
		n, addr, err := ServConn.ReadFromUDP(buf)
		fmt.Println("Received ", string(buf[0:n]), " from ", addr)

		if err != nil {
			fmt.Println("Error: ", err)
		}
	}
	//Loop infinito
	// for {
	// 	//Ler (uma vez somente) da conexão UDP a mensagem
	// 	//Escrever na tela a msg recebida (indicando o endereço de quem enviou)
	// }
}
func doClientJob(otherProcess int, i int) {
	//Enviar uma mensagem (com valor i) para o servidor do processo
	//otherServer
	msg := strconv.Itoa(i)
	buf := []byte(msg)
	_, err := CliConn[otherProcess].Write(buf)
	if err != nil {
		fmt.Println(msg, err)
	}
	time.Sleep(time.Second * 1)
}

func initConnections() {
	/*Esse 2 tira o nome (no caso Process) e tira a primeira porta
	(que é a minha). As demais portas são dos outros processos*/
	myPort = os.Args[1]
	nServers = len(os.Args) - 2
	// fmt.Println("Flag01")
	// fmt.Println("Server: ", "127.0.0.1"+os.Args[1])
	//Outros códigos para deixar ok a conexão do meu servidor (onde recebo msgs). O processo já deve ficar habilitado a receber msgs.
	ServerAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1"+os.Args[1])
	CheckError(err)

	ServConn, err = net.ListenUDP("udp", ServerAddr)
	CheckError(err)
	//Outros códigos para deixar ok as conexões com os servidores dos outros processos. Colocar tais conexões no vetor CliConn.
	for i := 0; i < nServers; i++ {
		// fmt.Println("Server para enviar: ", "127.0.0.1"+os.Args[i+2])
		CliAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1"+os.Args[i+2])
		CheckError(err)
		LocalAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
		CheckError(err)
		Conn, err := net.DialUDP("udp", LocalAddr, CliAddr)
		CheckError(err)
		CliConn = append(CliConn, Conn)
	}
}

func readInput(ch chan string) {
	// Non-blocking async routine to listen for terminal input
	reader := bufio.NewReader(os.Stdin)
	for {
		text, _, _ := reader.ReadLine()
		ch <- string(text)
	}
}

func main() {
	initConnections()
	// fmt.Println("Main Flag01")
	//O fechamento de conexões deve ficar aqui, assim só fecha
	//conexão quando a main morrer
	defer ServConn.Close()
	// fmt.Println("Main Flag02")
	for i := 0; i < nServers; i++ {
		// fmt.Println("Main Flag03")
		defer CliConn[i].Close()
	}
	//Todo Process fará a mesma coisa: ficar ouvindo mensagens e mandar infinitos i’s para os outros processos
	// fmt.Println("Main Flag04")
	go doServerJob()
	// fmt.Println("Main Flag05")
	i := 0
	for {
		// fmt.Println("Main Flag06")
		for j := 0; j < nServers; j++ {
			// fmt.Println("Main Flag07")
			go doClientJob(j, i)
		}
		// fmt.Println("Main Flag08")
		// Wait a while
		time.Sleep(time.Second * 1)
		i++
	}
}
