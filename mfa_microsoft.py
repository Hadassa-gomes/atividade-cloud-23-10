#!/usr/bin/env python3
"""
Exemplo: gerar TOTP (pyotp) + QR Code para Microsoft Authenticator.
Uso educativo — ajuste armazenamento/segurança para produção.
"""

import pyotp
import qrcode
import getpass
import os

# 1. Gerar chave secreta (Base32)
secret = pyotp.random_base32()
# Em ambiente real: não imprima a chave; salve-a de forma segura (DB, kms, etc).
print(" Chave secreta do usuário (apenas para testes):", secret)

# 2. Criar URI de provisionamento compatível com apps como Microsoft Authenticator
usuario = "aluno@teste.com"
emissor = "PraticaMFA-Microsoft"
totp = pyotp.TOTP(secret)
uri = totp.provisioning_uri(name=usuario, issuer_name=emissor)

# 3. Gerar QR Code para escanear no app
out_path = "qrcode_microsoft.png"
qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(uri)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save(out_path)
print(f" QR Code gerado: {out_path} — escaneie no Microsoft Authenticator.")

# 4. Simulação de login com senha + código TOTP
# Use getpass para não exibir a senha no terminal
senha_correta = "senha123"
senha = getpass.getpass(" Digite sua senha: ")

if senha == senha_correta:
    codigo = input(" Digite o código do Microsoft Authenticator (6 dígitos): ").strip()
    # Recomenda-se usar um small window para tolerância de clock (ex.: 1)
    # Isso aceita o código atual ± 1 passo (30s padrão).
    if totp.verify(codigo, valid_window=1):
        print(" Acesso permitido! MFA com Microsoft Authenticator bem-sucedido.")
    else:
        print(" Código incorreto ou expirado. Acesso negado.")
else:
    print(" Senha incorreta. Tente novamente.")
