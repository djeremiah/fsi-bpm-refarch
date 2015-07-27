package org.jbpm.examples.cmd;

import org.kie.api.runtime.process.WorkItem;
import org.kie.internal.executor.api.Command;
import org.kie.internal.executor.api.CommandContext;
import org.kie.internal.executor.api.ExecutionResults;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SimulatedServiceCallCommand implements Command {
    
    private static final Logger logger = LoggerFactory.getLogger(UserCommand.class);

    public ExecutionResults execute(CommandContext ctx) {
        logger.info("Command executed on executor with data {}", ctx.getData());
        WorkItem workItem = (WorkItem) ctx.getData("workItem");

        Long msDelay = Long.parseLong((String)workItem.getParameter("serviceMsDelay"));
        Integer retryTarget = (Integer)workItem.getParameter("serviceRetryTarget");
        Integer retryCount = (Integer)workItem.getParameter("serviceRetryCount");
        
        if(retryCount == null)
        	retryCount = 0;
        
        retryCount++;

        logger.info("Delaying for " + msDelay + " milliseconds on retry " + retryCount + " of " + retryTarget);
        try {
			Thread.sleep(msDelay);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
        logger.info(msDelay + " millisecond delay complete on retry " + retryCount + " of " + retryTarget);
        
        ctx.setData("serviceRetryCount", retryCount);
        
        ExecutionResults executionResults = new ExecutionResults();
        
        if(retryCount == retryTarget)
        	executionResults.setData("serviceStatus", "complete");
        
        return executionResults;
    }
    
}
