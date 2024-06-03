package $package;

import net.snackbag.cottonpowered.api.types.Identifier;

public enum $class {
	$materials;

	private final String i18n;
	private final Material material;

	$class(Material material, String i18n) {
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