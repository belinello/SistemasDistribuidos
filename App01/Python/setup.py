"""Constantes utilizadas no programa"""

### Constantes relativas à conexao 
MULTICAST_ADDR = '224.0.0.0'
BIND_ADDR = '0.0.0.0' # Bind to all interfaces in the system
PORT = 3000

#### Constantes relativas ao header da mensagem
# Header:   UUID | Porta unicast | Tipo mensagem | Tamanho mensagem | 
# UUID
UUID_BYTES = 32 + 4 # UUID tem 128bits = 32bytes. Alem disso tem 4bytes para separadores
UUID_RANGE = slice(0,UUID_BYTES) # Logo na mensagem o UUID esta na faixa [0:36]

# Porta unicast
PORT_RANGE = slice(UUID_RANGE.stop, UUID_RANGE.stop + 5) # 5 caracteres logo apos UUID

# Tipo mensagem
MSG_TYPE_RANGE = slice(PORT_RANGE.stop , PORT_RANGE.stop + 1) # Tipo da mensagem tem 1 char apenas 
MSG_TYPE_PUBKEY = "0"
MSG_TYPE_NORMAL = "2"


# Tamanho mensagem
import math
MSG_MAX_CHAR = 10000 # Numero maximo de caracteres da mensagem
MAX_NUMBER_DIGITS_MSG = int(math.log10(MSG_MAX_CHAR)) + 1  # Numero de char/digitos necessarios para representar o tamanho da mensagem. Exemplo: Se a mensagem tiver 2487 caracteres, para representar tal tamanho precisamos de 4 caracteres ('2','4','8','7')
MSG_SIZE_RANGE = slice(MSG_TYPE_RANGE.stop, MSG_TYPE_RANGE.stop + MAX_NUMBER_DIGITS_MSG) 

# Inicio da mensagem em si
MSG_START_BYTE = MSG_SIZE_RANGE.stop
