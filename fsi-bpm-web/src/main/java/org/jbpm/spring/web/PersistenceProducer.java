package org.jbpm.spring.web;

import javax.enterprise.context.ApplicationScoped;
import javax.enterprise.inject.Produces;
import javax.persistence.EntityManagerFactory;
import javax.persistence.PersistenceUnit;

import org.jbpm.runtime.manager.impl.jpa.EntityManagerFactoryManager;

@ApplicationScoped
public class PersistenceProducer {
    
    static {
        if ( System.getProperty( "org.kie.deployment.desc.location" ) == null ) {
            System.setProperty( "org.kie.deployment.desc.location", "classpath:META-INF/kie-wb-deployment-descriptor.xml" );
        }
    }
    
    @PersistenceUnit(unitName = "org.jbpm.domain")
    private EntityManagerFactory emf;

    @Produces
    public EntityManagerFactory getEntityManagerFactory() {
        if ( this.emf == null ) {
            // this needs to be here for non EE containers          
            this.emf = EntityManagerFactoryManager.get().getOrCreate("org.jbpm.domain");

        }
        return this.emf;
    }
}
