/*
 * Manba: https://github.com/spring-projects/spring-petclinic, commit 500158f,
 * src/main/java/org/springframework/samples/petclinic/owner/Visit.java.
 * Qisqartirilgan: maydonlar va annotatsiyalar qoldi, metodlar olib tashlandi.
 *
 * Copyright 2012-2025 the original author or authors.
 * Licensed under the Apache License, Version 2.0:
 * https://www.apache.org/licenses/LICENSE-2.0
 */
package org.springframework.samples.petclinic.owner;

import java.time.LocalDate;

import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.samples.petclinic.model.BaseEntity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

@Entity
@Table(name = "visits")
public class Visit extends BaseEntity {

	@Column(name = "visit_date")
	@DateTimeFormat(pattern = "yyyy-MM-dd")
	private LocalDate date;

	@NotBlank
	@Size(max = 255)
	private String description;

}
