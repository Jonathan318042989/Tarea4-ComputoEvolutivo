
class Codificacion:
    @staticmethod
    def decodifica_vector(x_cod, nBit, a, b):
        """
        Decodifica una lista de bits en una lista de valores reales según la codificación dada.

        Args:
        * x_cod: Lista de bits a decodificar.
        * nBit: Número de bits utilizados en la codificación.
        * a: Límite inferior del rango de valores a decodificar.
        * b: Límite superior del rango de valores a decodificar.

        Returns:
        * list: Lista de valores decodificados.
        """
        valor_decod = []
        for i in range(0, len(x_cod), nBit):
            sub_codificacion = x_cod[i:i+nBit]
            valor_decod.append(Codificacion.decodifica(sub_codificacion, nBit, a, b))
        return valor_decod

    @staticmethod
    def codifica_vector(x, nBit, a, b):
        """
        Codifica una lista de valores reales en una lista de bits según la codificación dada.

        Args:
        * x: Lista de valores a codificar.
        * nBit: Número de bits a utilizar en la codificación.
        * a: Límite inferior del rango de valores a codificar.
        * b: Límite superior del rango de valores a codificar.

        Returns:
        * list: Lista de bits resultante.
        """
        codificacion = []
        for val in x:
            if isinstance(val, int):
                codificacion.extend(Codificacion.codifica(val, nBit, a, b))
            elif isinstance(val, float):
                signo, float_bin = Codificacion.float_a_binario(val)
                codificacion.append(int(signo))
                codificacion.extend([int(bit) for bit in float_bin if bit != '.'])
            else:
                raise ValueError("Los valores deben ser enteros o flotantes.")
        return codificacion

    @staticmethod
    def decodifica(sub_codificacion, nBit, a, b):
        """
        Decodifica un subconjunto de bits en un valor real según la codificación dada.

        Args:
        * sub_codificacion: Subconjunto de bits a decodificar.
        * nBit: Número de bits utilizados en la codificación.
        * a: Límite inferior del rango de valores a decodificar.
        * b: Límite superior del rango de valores a decodificar.

        Returns:
        * float: Valor decodificado.
        """
        numero_int = int(''.join(str(bit) for bit in sub_codificacion), 2)
        return a + numero_int * (b - a) / ((2**nBit) - 1)

    @staticmethod
    def codifica(x, nBit, a, b):
        """
        Codifica un valor real en una lista de bits según la codificación dada.

        Args:
        * x: Valor a codificar.
        * nBit: Número de bits a utilizar en la codificación.
        * a: Límite inferior del rango de valores a codificar.
        * b: Límite superior del rango de valores a codificar.

        Returns:
        * list: Lista de bits resultante.
        """
        valor = (x - a) / (b - a)
        numero_int = int(valor * ((2**nBit) - 1))
        return [int(bit) for bit in bin(numero_int)[2:].zfill(nBit)]

    @staticmethod
    def float_a_binario(float_num):
        """
        Convierte un número de punto flotante en su representación binaria según el estándar IEEE 754.

        Args:
        * float_num: Número de punto flotante a convertir.

        Returns:
        * tuple: Tupla con el signo del número y su representación binaria.
        """
        signo = '0' if float_num >= 0 else '1'
        entero = abs(int(float_num))
        fracc = abs(float_num) - entero
        entero_binario = bin(entero)[2:]
        fracc_binario = ''
        while fracc != 0:
            fracc *= 2
            bit = '1' if fracc >= 1 else '0'
            fracc_binario += bit
            fracc -= int(bit)
        float_bin = entero_binario + '.' + fracc_binario
        return signo, float_bin