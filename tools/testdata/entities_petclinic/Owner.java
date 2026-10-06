/*
 * Manba: https://github.com/spring-projects/spring-petclinic, commit 500158f,
 * src/main/java/org/springframework/samples/petclinic/owner/Owner.java.
 * Qisqartirilgan: maydonlar va annotatsiyalar qoldi, metodlar olib tashlandi.
 * Sinov: @OneToMany + @JoinColumn(name = "owner_id") FK ni pets jadvaliga
 * beradi, bog'lovchi jadval yo'q (schema.sql: pets.owner_id).
 *
 * Copyright 2012-2025 the original author or authors.
 * Licensed under the Apache License, Version 2.0:
 * https://www.apache.org/licenses/LICENSE-2.0
 */
package org.springframework.samples.petclinic.owner;

import java.util.ArrayList;
import java.util.List;

import org.springframework.samples.petclinic.model.Person;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToMany;
import jakarta.persistence.OrderBy;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

@Entity
@Table(name = "owners")
public class Owner extends Person {

	@Column
	@NotBlank
	@Size(max = 255)
	private String address;

	@Column
	@NotBlank
	@Size(max = 80)
	private String city;

	@Column
	@NotBlank
	@Pattern(regexp = "\\d{10}", message = "{telephone.invalid}")
	private String telephone;

	@OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER)
	@JoinColumn(name = "owner_id")
	@OrderBy("name")
	private final List<Pet> pets = new ArrayList<>();

	public List<Pet> getPets() {
		return this.pets;
	}

}
