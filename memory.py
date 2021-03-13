####### Descricao / Description ##########
# Esse eh um programa simples apenas para demonstrar como acessar a memoria e deletar informacoes dela
# This is a simple program just to demostrate how to access memory and delete all data from there
##########################################

####### Agradecimento ##########
# Obrigado ao canal Labcode no youtube! O código foi escrito por eles, eu apenas achei muito interessante e decidi salva-lo.
# Thanks to Labcode channel at youtube! The code was wrote for them, I just liked this and saved it.
################################

# glbessa repository
# https://github.com/glbessa/ManageMem
# https://github.com/glbessa
# olhe alguns dos meus projetos, se tiver alguma ideia por favor me chame
# look at some of my projects, if you have an ideia please call me
# email: gabrielleitebessa@gmail.com


# bib ctypes
# ctypes library
import ctypes
# bib com funcoes do sistema
# system library
import sys
# coletor de lixo do python
# garbage collector
import gc

# representacao de uma variavel string do python no ctypes
# representation of python string in ctypes
class _PyStringObject(ctypes.Structure):
	# campos?
	# eu nao sei exatamente o que significa cada coisa
	# i dont know what each thing exactly mean
	fields = [
		('ob_refcnt', ctypes.c_ssize_t),
		('ob_type', ctypes.py_object),
		('ob_size', ctypes.c_ssize_t)
	]

# funcao para limpar a variavel da memoria
# function to clear the variable in the memory
def _clear_string(text:str):
	# salva o tamanho da string
	# save the size of the string
	size = len(text)

	# calcula a posicao exata
	# calculate string header offset
	location = id(text) + sys.getsizeof(text) - (size + 1)

	# representa a string do python em um objeto ctypes
	# represent the string at python in an ctypes object
	s_obj = _PyStringObject.from_address(id(text)) # do endereco de onde esta salva a variavel

	# limpa a informacao a respeito do tamanho da variavel
	# clear the information about string len
	s_obj.ob_size = 0

	# sobreescreve a variavel na memoria com 0x0 (\x00)
	# write on the variable at memory with 0x0 (\x00)
	ctypes.memset(location, 0x0, size)

# alguns experimentos com decoradores
# some expirement with decorators
def clear_specific(*keys_to_clear):
	def decorator(function):
		def wrapper(*args, **kwargs):
			ret = function(*args, **kwargs)
			for key in keys_to_clear:
					if key in kwargs and type(kwargs[key]) is str:
						_clear_string(kwargs[key])
			return ret
		return wrapper
	return decorator

# o mesmo que em cima
# the same that abouve
@clear_specific('password')
def save_password(*, password:str):
	print(password)
	print('saving password')

def another_test(secret:str):
	location = id(secret) + sys.getsizeof(secret) - (size + 1)
	print(hex(location))

# secret that is essecial to be out of mem after the program
# segredo que eh essecial estar fora da memoria depois de rodar o programa
secret = 'password'

# experiencia
# expirience
save_password(password=secret)

size = len(secret)

location = id(secret) + sys.getsizeof(secret) - (size + 1)

print(secret)
print(f'location: {hex(location)}')
print(ctypes.string_at(location, size))
another_test(secret)

# essa funcao apenas limpa a referencia da variavel do python, sem limpar seu conteudo
# this function just clear the reference to the variable at python, without clear its content
#del(secret)

# chama a funcao para limpar a frase na memoria
# call function to clear the string in memory
_clear_string(secret)

# NOTE que a referencia a variavel ainda existe no python
# NOTE that the reference to the variable exists in the program yet

# demonstra que a localizacao na memoria ainda existe
# demonstrate that the location in memory exists yet
print(f'location after deleting reference: {hex(location)}')

# acessa a memoria na posicao LOCATION e com o tamanho SIZE
# access memory in the position LOCATION and with lenght SIZE
print(ctypes.string_at(location, size))
# saida: | output:
# b'password'

print(secret)

input()
