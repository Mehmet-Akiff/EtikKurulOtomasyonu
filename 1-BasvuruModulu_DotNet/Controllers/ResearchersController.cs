using Microsoft.AspNetCore.Mvc;
using EtikKurul.BasvuruModulu.DTOs;
using EtikKurul.BasvuruModulu.Services;

namespace EtikKurul.BasvuruModulu.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ResearchersController : ControllerBase
{
    private readonly IApplicationService _service;

    public ResearchersController(IApplicationService service)
    {
        _service = service;
    }

    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var list = await _service.GetAllResearchersAsync();
        return Ok(list);
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(int id)
    {
        var researcher = await _service.GetResearcherByIdAsync(id);
        if (researcher == null) return NotFound(new { message = "Araştırmacı bulunamadı." });
        return Ok(researcher);
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateResearcherDto dto)
    {
        if (string.IsNullOrWhiteSpace(dto.FullName) || string.IsNullOrWhiteSpace(dto.Email))
        {
            return BadRequest(new { message = "Ad soyad ve e-posta zorunludur." });
        }

        var researcher = await _service.CreateResearcherAsync(dto);
        return CreatedAtAction(nameof(GetById), new { id = researcher.Id }, researcher);
    }
}
