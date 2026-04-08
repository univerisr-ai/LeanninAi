# EIP-152: Zcash Kanıtlarını Ethereum Üzerinde Doğrulama

## Meta
- status: draft-review
- category: frontend
- confidence: 85
- novelty: 88
- model: minimax/minimax-m2.7
- source: https://dev.to/zknd3r/verifying-zcash-proofs-on-ethereum-with-eip-152-4h80
- source_name: devto
- generated_at: 2026-04-08T02:56:28+00:00

## Ozet
EIP-152, Ethereum blockchain'inde Zcash'in BLS12-381 eliptik eğri kanıtlarını doğrulamak için kullanılan bir precompile'dir. 0x09 adresinde bulunan bu precompile, Ethereum akıllı sözleşmelerinin Zcash'in sıfır-bilgi kanıtlarını (ZK-SNARKs) doğrulamasına olanak tanır. Geliştiriciler cross-chain uygulamalarında zincirler arası köprüleme, gizlilik korumalı token transferleri ve merkeziyetsiz kimlik doğrulama sistemleri oluşturabilir. Bu precompile, özellikle Zcash'in privacy özelliklerini Ethereum'un Turing-tam sözleşme ortamıyla birleştirmek isteyen projeler için kritik öneme sahiptir.

## Ana Noktalar
- 0x09 adresindeki EIP-152 precompile'ı BLS12-381 eğri operasyonlarını gerçekleştirir
- Zcash'in Groth16 ve PLONK gibi sıfır-bilgi kanıt sistemlerini Ethereum üzerinde doğrulayabilir
- Pairing işlemleri için optimize edilmiş bls12_cyclegroeth ve bls12_cyclegroep precompile fonksiyonları sunar
- Cross-chain köprüleme ve zincirler arası gizlilik transferleri için temel altyapı sağlar
- Gas maliyeti yüksek olabilir; on-chain doğrulama yerine off-chain kanıt üretimi önerilir
- Merkeziyetsiz kimlik (DID) ve attestation sistemlerinde kanıt doğrulama için kullanılabilir

## Iliskili Sayfalar
- [[XSS ve CSRF Açıkları]]
- [[JWT ve Kimlik Doğrulama]]
- [[Bot Tespiti ve Honeypot (Bal Küpü)]]

## Kaynak Basligi
Verifying Zcash Proofs on Ethereum with EIP-152
