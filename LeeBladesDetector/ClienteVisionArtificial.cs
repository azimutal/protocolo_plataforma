using System.Buffers.Binary;
using System.Diagnostics;
using System.Net;
using System.Net.Sockets;

namespace LeeBladesDetector;

public class ClienteVisionArtificial(string ip, int puertoControl = 8208, int puertoStreaming = 8206)
    : IDisposable
{
    private const int MensajeEstablecerMensajesPorSegundo = 1;
    private const int MensajeComenzarStreaming = 2;
    private const int MensajeFinalizarStreaming = 3;
    private const int TamanoMensaje = 40;

    private UdpClient? clienteStreaming;
    private CancellationTokenSource? cts;
    public event EventHandler<DatosStreaming>? PaqueteRecibido;

    public void Start()
    {
        if (cts is not null)
            throw new InvalidOperationException("El cliente ya está en marcha.");

        clienteStreaming = new UdpClient(puertoStreaming);
        cts = new CancellationTokenSource();

        EnviarComandoControl(MensajeEstablecerMensajesPorSegundo, 200);
        EnviarComandoControl(MensajeComenzarStreaming);

        Task.Run(() => BucleRecepcion(cts.Token));
    }

    public void Stop()
    {
        if (cts is null) 
            return;

        EnviarComandoControl(MensajeFinalizarStreaming);

        cts.Cancel();
        clienteStreaming?.Close();
        cts = null;
        clienteStreaming = null;
    }

    public void Dispose() => Stop();

    private void EnviarComandoControl(int comando, float parámetro=0.0f)
    {
        var mensaje = new byte[8];
        BinaryPrimitives.WriteInt32LittleEndian(mensaje.AsSpan(0, 4), comando);
        BinaryPrimitives.WriteSingleLittleEndian(mensaje.AsSpan(4, 4), parámetro);

        using var clienteControl = new UdpClient();
        clienteControl.Send(mensaje, mensaje.Length, ip, puertoControl);
    }

    private async Task BucleRecepcion(CancellationToken token)
    {
        var remoto = new IPEndPoint(IPAddress.Any, 0);

        while (!token.IsCancellationRequested)
        {
            try
            {
                var resultado = await clienteStreaming!.ReceiveAsync(token);
                var datos = resultado.Buffer;


                if (datos.Length < TamanoMensaje)
                {
                    Trace.WriteLine($"[AVISO] Paquete demasiado corto: {datos.Length} bytes.");
                    continue;
                }

                var span = datos.AsSpan();
                var paquete = new DatosStreaming
                {
                    Timestamp = BinaryPrimitives.ReadDoubleLittleEndian(span.Slice(0, 8)),
                    Yaw = BinaryPrimitives.ReadSingleLittleEndian(span.Slice(8, 4)),
                    Pitch = BinaryPrimitives.ReadSingleLittleEndian(span.Slice(12, 4)),
                    Roll0 = BinaryPrimitives.ReadSingleLittleEndian(span.Slice(16, 4)),
                    Roll1 = BinaryPrimitives.ReadSingleLittleEndian(span.Slice(20, 4)),
                    Roll2 = BinaryPrimitives.ReadSingleLittleEndian(span.Slice(24, 4)),
                    Cuarto0 = BinaryPrimitives.ReadSingleLittleEndian(span.Slice(28, 4)),
                    Cuarto1 = BinaryPrimitives.ReadSingleLittleEndian(span.Slice(32, 4)),
                    Cuarto2 = BinaryPrimitives.ReadSingleLittleEndian(span.Slice(36, 4)),
                };

                PaqueteRecibido?.Invoke(this, paquete);
            }
            catch (SocketException) when (token.IsCancellationRequested)
            {
                // Cierre normal al llamar a Stop()
                break;
            }
        }
    }
}