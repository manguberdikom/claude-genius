/*
 * Manba: https://github.com/spring-projects/spring-petclinic, commit 500158f,
 * src/main/java/org/springframework/samples/petclinic/model/NamedEntity.java.
 * Qisqartirilgan: maydonlar va annotatsiyalar qoldi, metodlar olib tashlandi.
 *
 * Copyright 2012-2025 the original author or authors.
 * Licensed under the Apache License, Version 2.0:
 * https://www.apache.org/licenses/LICENSE-2.0
 */
package org.springframework.samples.petclinic.model;

import jakarta.persistence.Column;
import jakarta.persistence.MappedSuperclass;
import jakarta.validation.constraints.NotBlank;

@MappedSuperclass
public class NamedEntity extends BaseEntity {

	@Column
	@NotBlank
	private String name;

}
