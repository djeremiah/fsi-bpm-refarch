package org.jbpm.spring;

import java.util.Collections;
import java.util.List;

import org.kie.internal.identity.IdentityProvider;


public class NoopIdentityProvider implements IdentityProvider {
	
	public String getName() {
		return "default";
	}

	public List<String> getRoles() {
		return Collections.emptyList();
	}

	public boolean hasRole(String role) {
		return false;
	}

}
