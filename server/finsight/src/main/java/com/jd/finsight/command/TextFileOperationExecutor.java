package com.jd.finsight.command;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class TextFileOperationExecutor {
    private final List<Command> textFileOperations = new ArrayList<>();

    public void executeOperation(Command command) {
        textFileOperations.add(command);
        command.execute();
    }
}
