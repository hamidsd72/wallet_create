from django.shortcuts import render
from django.http import JsonResponse
from pywallet import wallet
import binascii
from bip_utils import MoneroWordsNum, MoneroMnemonicGenerator, MoneroSeedGenerator, Monero

def setWallet(type="ETH"):
    seed = wallet.generate_mnemonic()
    return wallet.create_wallet(network=type, seed=seed, children=1)

def Home(request):
    mnemonic = MoneroMnemonicGenerator().FromWordsNumber(MoneroWordsNum.WORDS_NUM_25)
    seed_bytes = MoneroSeedGenerator(mnemonic).Generate()
    monero = Monero.FromSeed(seed_bytes)
    payment_id = binascii.unhexlify(b"d6f093554c0daa94")
    print(monero)
    data = {
        "name":             "monero",
        "privateSpendKey":   monero.PrivateSpendKey().Raw().ToHex(),
        "privateViewKey":    monero.PrivateViewKey().Raw().ToHex(),
        "publicSpendKey":    monero.PublicSpendKey().RawCompressed().ToHex(),
        "publicViewKey":     monero.PublicViewKey().RawCompressed().ToHex(),
        "primaryAddress":    monero.PrimaryAddress(), # == monero.Subaddress(0, 0)
        "integratedAddress": monero.IntegratedAddress(payment_id),
        "subaddress":        monero.Subaddress(1, 0)
    }
    templateName = "wallet/home.html"
    return render(request, templateName, data)

def SetWallet(request, slug):
    try:
        d = setWallet(slug)
        data = {
            "name":         slug,
            "address":      d["address"],
            "private_key":  d["private_key"],
            "public_key":   d["public_key"],
            "childrenAddr": d["children"][0]["address"],
            "childrenPubK": d["children"][0]["xpublic_key"]
        }
        templateName = "wallet/home.html" 
        return render(request, templateName, data)
    except:
        return 'find wallet using this slug wrong...'
