package com.jd.finsight.command;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class CommandOperationExecutor {
    // only safe to use List for ops in single-threaded app (concurrency)
    private final List<Command> commandList = new ArrayList<>();

    public void executeOperation(Command command) {
        commandList.add(command);
        command.execute();
    }

    // can add additional commands for undo, redo, etc.
}