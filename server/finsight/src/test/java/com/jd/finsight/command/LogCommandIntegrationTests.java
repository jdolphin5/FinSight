package com.jd.finsight.command;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.File;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import com.jd.finsight.logging.impl.CommandLogGenerator;

@SpringBootTest
@ExtendWith(SpringExtension.class)
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
public class LogCommandIntegrationTests {

    // command
    private Command logCommand;

    // receiver
    private CommandHandler commandHandler;

    // invoker
    private CommandOperationInvoker commandOperationInvoker;

    public LogCommandIntegrationTests() {
        this.commandHandler = new CommandHandler();
        this.logCommand = new LogCommand("test log", commandHandler, new CommandLogGenerator("test.txt"));
        this.commandOperationInvoker = new CommandOperationInvoker();
    }

    @AfterEach
    public void cleanUp() {
        // Clean up the log file after each test
        File logFile = new File("test.txt");
        if (logFile.exists()) {
            logFile.delete(); // Deletes the file created during the test
        }
    }

    @Test
    public void testThatLogCommandCreatesLogFileWhenLogCommandIsInvoked() {
        commandOperationInvoker.invokeCommand(logCommand);

        File logFile = new File("test.txt");
        assertTrue(logFile.exists(), "Log file should be created");
    }

}
