import io from 'socket.io-client'

class SocketioService {
    socket;
    constructor() { }

    setupSocketConnection() {
        this.socket = io("localhost:3000")
    }
}

export default new SocketioService();