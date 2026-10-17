using Microsoft.AspNetCore.Mvc;
using EtikKurul.BasvuruModulu.DTOs;
using EtikKurul.BasvuruModulu.Services;

namespace EtikKurul.BasvuruModulu.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ApplicationsController : ControllerBase
{
    private readonly IApplicationService _service;

    public ApplicationsController(IApplicationService service)
    {
        _service = service;
    }

    [HttpGet]
    public async Task<IActionResult> GetAll([FromQuery] string? status)
    {
        var list = await _service.GetAllApplicationsAsync(status);
        return Ok(list);
    }

    [HttpGet("{id:int}")]
    public async Task<IActionResult> GetById(int id)
    {
        var app = await _service.GetApplicationByIdAsync(id);
        if (app == null) return NotFound(new { message = $"Başvuru #{id} bulunamadı." });
        return Ok(app);
    }

    [HttpGet("protocol/{protocolNumber}")]
    public async Task<IActionResult> GetByProtocol(string protocolNumber)
    {
        var app = await _service.GetApplicationByProtocolAsync(protocolNumber);
        if (app == null) return NotFound(new { message = $"Protokol no {protocolNumber} ile başvuru bulunamadı." });
        return Ok(app);
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateApplicationDto dto)
    {
        if (string.IsNullOrWhiteSpace(dto.ProjectTitle) || dto.ResearcherId <= 0)
        {
            return BadRequest(new { message = "Proje başlığı ve geçerli bir araştırmacı seçilmelidir." });
        }

        try
        {
            var result = await _service.CreateApplicationAsync(dto);
            return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
        }
        catch (ArgumentException ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    [HttpPost("{id:int}/documents")]
    public async Task<IActionResult> UploadDocument(int id, [FromBody] UploadDocumentDto dto)
    {
        if (string.IsNullOrWhiteSpace(dto.DocumentType) || string.IsNullOrWhiteSpace(dto.FileName))
        {
            return BadRequest(new { message = "Belge türü ve dosya adı zorunludur." });
        }

        try
        {
            var result = await _service.UploadDocumentAsync(id, dto);
            return Ok(result);
        }
        catch (ArgumentException ex)
        {
            return NotFound(new { message = ex.Message });
        }
    }

    [HttpPost("{id:int}/submit")]
    public async Task<IActionResult> Submit(int id)
    {
        try
        {
            var result = await _service.SubmitApplicationAsync(id);
            return Ok(new
            {
                message = "Etik kurul başvurusu başarıyla onaya sunuldu.",
                application = result
            });
        }
        catch (ArgumentException ex)
        {
            return NotFound(new { message = ex.Message });
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    [HttpPatch("{id:int}/status")]
    public async Task<IActionResult> UpdateStatus(int id, [FromBody] UpdateStatusDto dto)
    {
        try
        {
            var result = await _service.UpdateStatusAsync(id, dto);
            return Ok(result);
        }
        catch (ArgumentException ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }
}
