package com.jd.finsight.command;

import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit.jupiter.SpringExtension;

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

    @Autowired
    public LogCommandIntegrationTests() {
    }

}