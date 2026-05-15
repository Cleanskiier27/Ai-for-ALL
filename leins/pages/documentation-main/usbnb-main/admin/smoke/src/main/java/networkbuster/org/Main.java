package networkbuster.org;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        int port = 8080;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        
        server.createContext("/", new MyHandler());
        server.setExecutor(null); // creates a default executor
        server.start();
        
        System.out.println("NetworkBuster OS Server started on port " + port);
    }

    static class MyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange t) throws IOException {
            String html = "<!DOCTYPE html>\n" +
"<html lang=\"en\">\n" +
"<head>\n" +
"    <meta charset=\"UTF-8\">\n" +
"    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n" +
"    <title>NetworkBuster OS - Access Terminal</title>\n" +
"    <style>\n" +
"        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');\n" +
"        :root {\n" +
"            --primary: #0ff;\n" +
"            --bg: #050510;\n" +
"            --glass: rgba(0, 255, 255, 0.03);\n" +
"        }\n" +
"        body {\n" +
"            margin: 0;\n" +
"            padding: 0;\n" +
"            background-color: var(--bg);\n" +
"            color: #fff;\n" +
"            font-family: 'Share Tech Mono', monospace;\n" +
"            display: flex;\n" +
"            justify-content: center;\n" +
"            align-items: center;\n" +
"            height: 100vh;\n" +
"            overflow: hidden;\n" +
"        }\n" +
"        .terminal {\n" +
"            background: var(--glass);\n" +
"            border: 1px solid rgba(0, 255, 255, 0.15);\n" +
"            padding: 50px;\n" +
"            border-radius: 8px;\n" +
"            box-shadow: 0 0 40px rgba(0, 255, 255, 0.05), inset 0 0 20px rgba(0, 255, 255, 0.02);\n" +
"            backdrop-filter: blur(10px);\n" +
"            text-align: center;\n" +
"            max-width: 450px;\n" +
"            width: 100%;\n" +
"            z-index: 10;\n" +
"        }\n" +
"        h1 {\n" +
"            color: var(--primary);\n" +
"            text-transform: uppercase;\n" +
"            letter-spacing: 5px;\n" +
"            margin-bottom: 5px;\n" +
"            font-size: 28px;\n" +
"            text-shadow: 0 0 15px rgba(0, 255, 255, 0.6);\n" +
"        }\n" +
"        p {\n" +
"            color: #66b3b3;\n" +
"            font-size: 14px;\n" +
"            margin-bottom: 40px;\n" +
"            letter-spacing: 1px;\n" +
"        }\n" +
"        .input-group {\n" +
"            margin-bottom: 25px;\n" +
"            text-align: left;\n" +
"        }\n" +
"        label {\n" +
"            display: block;\n" +
"            color: var(--primary);\n" +
"            margin-bottom: 8px;\n" +
"            font-size: 13px;\n" +
"            letter-spacing: 2px;\n" +
"        }\n" +
"        input[type=\"password\"] {\n" +
"            width: 100%;\n" +
"            padding: 15px;\n" +
"            background: rgba(0, 20, 20, 0.6);\n" +
"            border: 1px solid rgba(0, 255, 255, 0.3);\n" +
"            color: var(--primary);\n" +
"            border-radius: 4px;\n" +
"            outline: none;\n" +
"            box-sizing: border-box;\n" +
"            font-family: inherit;\n" +
"            font-size: 18px;\n" +
"            letter-spacing: 10px;\n" +
"            text-align: center;\n" +
"            transition: border-color 0.3s ease, box-shadow 0.3s ease;\n" +
"        }\n" +
"        input[type=\"password\"]:focus {\n" +
"            border-color: var(--primary);\n" +
"            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);\n" +
"        }\n" +
"        button {\n" +
"            width: 100%;\n" +
"            padding: 16px;\n" +
"            background: rgba(0, 255, 255, 0.05);\n" +
"            color: var(--primary);\n" +
"            border: 1px solid var(--primary);\n" +
"            cursor: pointer;\n" +
"            font-family: inherit;\n" +
"            font-weight: bold;\n" +
"            font-size: 16px;\n" +
"            letter-spacing: 3px;\n" +
"            text-transform: uppercase;\n" +
"            transition: all 0.3s ease;\n" +
"            border-radius: 4px;\n" +
"        }\n" +
"        button:hover {\n" +
"            background: var(--primary);\n" +
"            color: #000;\n" +
"            box-shadow: 0 0 25px var(--primary);\n" +
"        }\n" +
"        .grid-bg {\n" +
"            position: absolute;\n" +
"            top: -50%; left: -50%; right: -50%; bottom: -50%;\n" +
"            background-image: \n" +
"                linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),\n" +
"                linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);\n" +
"            background-size: 50px 50px;\n" +
"            z-index: 0;\n" +
"            transform: perspective(500px) rotateX(60deg) translateY(-100px) translateZ(-200px);\n" +
"            animation: moveGrid 20s linear infinite;\n" +
"        }\n" +
"        @keyframes moveGrid {\n" +
"            0% { transform: perspective(500px) rotateX(60deg) translateY(0) translateZ(-200px); }\n" +
"            100% { transform: perspective(500px) rotateX(60deg) translateY(50px) translateZ(-200px); }\n" +
"        }\n" +
"        .scanline {\n" +
"            width: 100%;\n" +
"            height: 100px;\n" +
"            z-index: 20;\n" +
"            position: absolute;\n" +
"            pointer-events: none;\n" +
"            background: linear-gradient(0deg, rgba(0,0,0,0) 0%, rgba(0,255,255,0.1) 50%, rgba(0,0,0,0) 100%);\n" +
"            opacity: 0.1;\n" +
"            animation: scanline 6s linear infinite;\n" +
"        }\n" +
"        @keyframes scanline {\n" +
"            0% { top: -100px; }\n" +
"            100% { top: 100%; }\n" +
"        }\n" +
"    </style>\n" +
"</head>\n" +
"<body>\n" +
"    <div class=\"grid-bg\"></div>\n" +
"    <div class=\"scanline\"></div>\n" +
"    <div class=\"terminal\">\n" +
"        <h1>NetworkBuster</h1>\n" +
"        <p>SECURE OS TERMINAL /// AWAITING AUTHORIZATION</p>\n" +
"        <div class=\"input-group\">\n" +
"            <label>ACCESS_CODE</label>\n" +
"            <input type=\"password\" id=\"passcode\" placeholder=\"****\" autocomplete=\"off\" />\n" +
"        </div>\n" +
"        <button onclick=\"alert('AUTHENTICATION PROTOCOL INITIATED...\\nUPLINK ESTABLISHED.')\">Initialize Sequence</button>\n" +
"    </div>\n" +
"</body>\n" +
"</html>";
            
            byte[] bytes = html.getBytes("UTF-8");
            t.getResponseHeaders().add("Content-Type", "text/html; charset=UTF-8");
            t.sendResponseHeaders(200, bytes.length);
            OutputStream os = t.getResponseBody();
            os.write(bytes);
            os.close();
        }
    }
}