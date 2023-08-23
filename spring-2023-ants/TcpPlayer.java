import java.io.*;
import java.net.Socket;
import java.net.SocketException;

public class TcpPlayer {
    private Socket clientSocket;
    private PrintWriter out;
    private BufferedReader in;
    private BufferedReader pipein;
    private PrintWriter pipeout;

    public TcpPlayer(InputStream stdin, PrintStream stdout, PrintStream stderr) {

        System.out.println("Connecting to 6666");
        try {

            clientSocket = new Socket("127.0.0.1", 6666);
            out = new PrintWriter(clientSocket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

            pipein = new BufferedReader(new InputStreamReader(stdin));
            pipeout = new PrintWriter(stdout, true);

            String line = pipein.readLine();
            out.println(line);

            int cells = Integer.parseInt(line);
            for (int i=0; i<cells; i++) {
                line = pipein.readLine();
                out.println(line);
            }
            line = pipein.readLine(); // bases
            out.println(line);
            line = pipein.readLine(); // mybase
            out.println(line);
            line = pipein.readLine(); // oppbase
            out.println(line);
            out.flush();

            // game
            while(true) {

                for (int i=0; i<cells; i++) {
                    line = pipein.readLine();
                    out.println(line);
                }
                out.flush();

                String play = in.readLine();
                pipeout.println(play);
                pipeout.flush();
            }

        } catch (Exception e) {
            stderr.println(e.toString());
            try {
                clientSocket.close();
            } catch (IOException se){
                stderr.println(se.toString());
            }
        }
    }
}
