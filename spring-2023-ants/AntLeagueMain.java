import com.codingame.gameengine.runner.MultiplayerGameRunner;
import com.codingame.gameengine.runner.simulate.GameResult;
import com.google.common.io.Files;
import com.google.gson.Gson;

import java.io.File;
import java.io.IOException;

public class AntLeagueMain {
    public static void main(String[] args) throws IOException, InterruptedException {

        MultiplayerGameRunner gameRunner = new MultiplayerGameRunner();
        if (args.length > 0) {
            long seed = Long.parseLong(args[0]);
            gameRunner.setSeed(seed);
            System.out.println("seed : " + seed);

        }
        // gameRunner.addAgent(TimeoutPlayer.class, "TestBoss_1");
        gameRunner.addAgent(TcpPlayer.class, "TestBoss_1");
        gameRunner.addAgent("python3 config/Qookie.py", "TestBoss_2");
        // gameRunner.setLeagueLevel(1);

        GameResult gameresult = gameRunner.simulate();
        String result = new Gson().toJson(gameresult);
        System.out.println("Result : " + result);

    }
}
