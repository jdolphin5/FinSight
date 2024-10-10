package com.jd.finsight.command;

import com.jd.finsight.logging.LogGenerator;

public class LogCommand extends Command {
    private String log;
    private CommandHandler commandHandler;
    LogGenerator logGenerator;

    public LogCommand(String log, CommandHandler commandHandler, LogGenerator logGenerator) {
        this.log = log;
        this.commandHandler = commandHandler;
        this.logGenerator = logGenerator;
    }

    @Override
    public void execute() {
        // open file
        // textFile.open();
        // write to new line in file
        // save file

        commandHandler.log(log, logGenerator);
    }

}
