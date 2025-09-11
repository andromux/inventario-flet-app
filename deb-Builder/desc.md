Hemos realizado mejoras en la aplicación de inventario para que sea más **robusta** y fácil de usar. Ahora, la navegación entre las páginas de **Ventas** y **Reportes** actualiza automáticamente sus datos para reflejar los cambios más recientes, eliminando la necesidad de reiniciar el programa. Además, la página de **Catálogo** valida los datos de entrada para evitar errores al añadir productos y acepta diferentes formatos numéricos. 


```bash
chmod +x inventario-linux_0.2.1_amd64.deb
sudo apt install ./inventario-linux_0.2.1_amd64.deb
```

1. **Descarga el `.deb`** → un paquete que contiene la aplicación ya empacada.
2. **Navegaste a la carpeta** donde estaba el archivo.

4. Como es un `.deb`, queda integrado en el sistema igual que cualquier otro paquete oficial.

---

## 🔹 ¿Cómo desinstalarlo?

Tienes dos opciones:

1. **Quitar solo el programa (conservar configuraciones en `/etc/`)**

   ```bash
   sudo apt remove inventario-linux
   ```

2. **Quitar completamente, incluidas configuraciones**

   ```bash
   sudo apt purge inventario-linux
   ```

3. **Ver qué instaló tu `.deb`**

   ```bash
   dpkg -L inventario-linux
   ```

4. **Eliminar dependencias sobrantes (opcional)**

   ```bash
   sudo apt autoremove
   ```

* **Debian / Ubuntu / Mint / Pop!\_OS** → se usa `apt install ./archivo.deb` (recomendado).
* **Distribuciones con `dpkg` puro (sin apt)** →

  ```bash
  sudo dpkg -i inventario-linux_0.2.1_amd64.deb
  sudo apt-get install -f   # arreglar dependencias si faltan
  ```
* **Distribuciones basadas en Fedora (RPM, no DEB)** → no funciona, ahí se usan `.rpm`.
