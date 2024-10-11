package com.jd.finsight.command;

import org.springframework.stereotype.Service;

import com.jd.finsight.logging.LogGenerator;

@Service
public class CommandHandler {

    public CommandHandler() {
    }

    public void log(String log, LogGenerator logGenerator) {
        logGenerator.createLogger();
        logGenerator.getLogger().writeLogsToFile(log);
    }

}
