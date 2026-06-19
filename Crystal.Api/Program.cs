var builder = WebApplication.CreateBuilder(args);

// Agrega los servicios de los controladores
builder.Services.AddControllers();

// 1. Esto le dice a tu API que genere la documentación de Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// 2. Esto enciende la interfaz web de Swagger si estás probando localmente
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();
app.Run();