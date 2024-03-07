package net.rozukke.elci;


import com.google.protobuf.Message;

import javax.crypto.Cipher;
import java.security.*;
import java.security.spec.*;
import java.util.Base64;

public class CryptographySession {
	public static final int keySize = 2048;
	public static final String CIPHER_INSTANCE_TYPE = "RSA";

	public final PrivateKey privateKey;
	public final PublicKey publicKey;
	public PublicKey recipientPublicKey;


	public CryptographySession() {
		System.out.println("Generating Cryptographic Key Pair");
		//Generate keys
		try {
			KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("RSA");
			keyPairGen.initialize(keySize);
			KeyPair pair = keyPairGen.generateKeyPair();

			this.privateKey = pair.getPrivate();
			this.publicKey = pair.getPublic();
		} catch (NoSuchAlgorithmException e) {
			throw new RuntimeException(e);
		}
	}

	public void setRecipientPublicKey(byte[] key){
		try {

			byte[] rawKey = Base64.getDecoder().decode(key);
			KeyFactory keyFactory = KeyFactory.getInstance("RSA");

			this.recipientPublicKey = keyFactory.generatePublic(new X509EncodedKeySpec(rawKey));
		}catch (GeneralSecurityException ex){
			ex.printStackTrace();
		}
	}

	public byte[] encrypt(byte[] data) {
		try {
			//encrypt with recipient public key
			Cipher cipherInstance = Cipher.getInstance(CIPHER_INSTANCE_TYPE);
			cipherInstance.init(Cipher.ENCRYPT_MODE, recipientPublicKey);

			byte[] out = cipherInstance.doFinal(data);
			return Base64.getEncoder().encode(out);
		}catch (GeneralSecurityException ex){
			ex.printStackTrace();
		}
		return null;
	}

	public byte[] decrypt(byte[] data){
		try {
			data = Base64.getDecoder().decode(data);
			//encrypt with recipient public key
			Cipher cipherInstance = Cipher.getInstance(CIPHER_INSTANCE_TYPE);
			cipherInstance.init(Cipher.DECRYPT_MODE, privateKey);

			return cipherInstance.doFinal(data);
		}catch (GeneralSecurityException ex){
			ex.printStackTrace();
		}
		return null;
	}

	public byte[] sign(byte[] message){

		try{

			Signature sign = Signature.getInstance("SHA256withRSA");
			sign.initSign(privateKey);
			byte[] bytes = message;
			sign.update(bytes);
			byte[] signature = sign.sign();
			return Base64.getEncoder().encode(signature);
		}catch (GeneralSecurityException ex){
			ex.printStackTrace();
		}
		return null;
	}

	public boolean verify(byte[] message, String signature){
		try{
			Signature sign = Signature.getInstance("SHA256withRSA");
			sign.initVerify(recipientPublicKey);
			byte[] bytes = message;
			sign.update(bytes);
			boolean bool = sign.verify(Base64.getDecoder().decode(signature.getBytes()));
			return bool;

		}catch (GeneralSecurityException ex){
			ex.printStackTrace();
		}
		return false;
	}




}


