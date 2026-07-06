.PHONY: run clean

run:
	@echo "Executando o simulador..."
	python3 simulatorProcessor.py

clean:
	@echo "Limpando os arquivos de saída..."
	rm -f unidade_controle.txt memoria_ram.txt banco_registradores.txt