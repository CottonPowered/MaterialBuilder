package net.snackbag.cottonpowered.api.material;

import net.snackbag.cottonpowered.api.types.Identifier;

public enum VanillaMaterial {
	$materials;

	private final String i18n;
	private final Material material;

	VanillaMaterial(Material material, String i18n) {
		this.material = material;
		this.i18n = i18n;
	}

	public Material getMaterial() {
		return material;
	}

	public String getI18n() {
		return i18n;
	}

	public boolean equals(Material material) {
		return getMaterial().equals(material);
	}
}