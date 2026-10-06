/*
 * Manba: https://github.com/spring-projects/spring-petclinic, commit 500158f,
 * src/main/java/org/springframework/samples/petclinic/owner/PetType.java.
 *
 * Copyright 2012-2025 the original author or authors.
 * Licensed under the Apache License, Version 2.0:
 * https://www.apache.org/licenses/LICENSE-2.0
 */
package org.springframework.samples.petclinic.owner;

import org.springframework.samples.petclinic.model.NamedEntity;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "types")
public class PetType extends NamedEntity {

}
