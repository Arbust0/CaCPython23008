fetch("https://dolar-api-argentina.vercel.app/v1/dolares")
  .then((response) => response.json())
  .then((json) => {
    let li = `<thead><tr><th>Nombre</th><th>Compra</th><th>Venta</th></tr></thead>`;

    json.forEach((obj) => 
    {
        if (obj.compra == null) {
           obj.compra = "";  
        }
      li += `<tbody><tr>
        <td>${obj.nombre}</td>
        <td>${obj.compra} </td>
        <td>${obj.venta}</td>
      </tr></tbody>`;
    });

    document.getElementById("cotizacion").innerHTML = li;
  });