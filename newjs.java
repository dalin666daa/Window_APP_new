import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class OrnamentDetectionUI extends Application {
    private Process pythonProcess;
    private TextArea consoleOutput;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Ornament Detection");

        // Layout components
        BorderPane root = new BorderPane();
        consoleOutput = new TextArea();
        consoleOutput.setEditable(false);

        ImageView cameraFeed = new ImageView();
        cameraFeed.setFitWidth(640);
        cameraFeed.setFitHeight(480);
        cameraFeed.setPreserveRatio(true);

        Button startButton = new Button("Start Detection");
        Button stopButton = new Button("Stop Detection");
        stopButton.setDisable(true);

        HBox controls = new HBox(10, startButton, stopButton);
        controls.setStyle("-fx-padding: 10; -fx-alignment: center;");

        root.setCenter(cameraFeed);
        root.setBottom(consoleOutput);
        root.setTop(controls);

        // Button Actions
        startButton.setOnAction(event -> {
            startDetection(cameraFeed);
            startButton.setDisable(true);
            stopButton.setDisable(false);
        });

        stopButton.setOnAction(event -> {
            stopDetection();
            startButton.setDisable(false);
            stopButton.setDisable(true);
        });

        // Scene and Stage setup
        Scene scene = new Scene(root, 800, 600);
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private void startDetection(ImageView cameraFeed) {
        try {
            // Launch Python process
            ProcessBuilder builder = new ProcessBuilder("python", "ornament_detection.py");
            builder.redirectErrorStream(true);
            pythonProcess = builder.start();

            // Read Python output and display in TextArea
            new Thread(() -> {
                try (BufferedReader reader = new BufferedReader(
                        new InputStreamReader(pythonProcess.getInputStream()))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        final String outputLine = line;
                        javafx.application.Platform.runLater(() -> consoleOutput.appendText(outputLine + "\n"));
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }).start();

            // Periodically update ImageView (dummy logic for now)
            new Thread(() -> {
                while (pythonProcess.isAlive()) {
                    javafx.application.Platform.runLater(() -> {
                        // Update camera feed with a placeholder image or actual feed
                        cameraFeed.setImage(new Image("file:placeholder.png"));
                    });
                    try {
                        Thread.sleep(1000 / 30); // Simulate 30 FPS
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            }).start();

        } catch (Exception e) {
            e.printStackTrace();
            consoleOutput.appendText("Error: Unable to start Python script.\n");
        }
    }

    private void stopDetection() {
        if (pythonProcess != null && pythonProcess.isAlive()) {
            pythonProcess.destroy();
            consoleOutput.appendText("Python script stopped.\n");
        }
    }
}
