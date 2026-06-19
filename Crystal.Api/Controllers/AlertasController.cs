using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace Crystal.Api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AlertasController : ControllerBase
    {
        private static List<string> _alertas = new List<string>
        {
            "Simulacion: Intento de acceso SSH fallido",
            "Simulacion: Modificacion de archivo host detectada"
        };

        [HttpGet]
        public IActionResult GetAlertas()
        {
            return Ok(_alertas);
        }

        [HttpPost]
        public IActionResult RegistrarAlerta([FromBody] string nuevaAlerta)
        {
            if (string.IsNullOrWhiteSpace(nuevaAlerta))
                return BadRequest("La alerta no puede estar vacía.");

            _alertas.Add(nuevaAlerta);
            return Ok(new { Mensaje = "Alerta centralizada", Alerta = nuevaAlerta });
        }
    }
}