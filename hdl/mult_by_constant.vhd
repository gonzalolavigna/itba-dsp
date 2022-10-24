--------------------------------------------------------------------------------
--
-- Title    : mult_by_constant.vhd
-- Project  : PDS 2020
-- Author   : GOnzalo Lavigna
-- Date     : 02/JUL/2020
--------------------------------------------------------------------------------
--
-- Description
-- Multiplicar poru nas constante un stream proveniente de AXI y devolverlo en AXIS.
-- Depende del usuario utilizar como corresponde el corrimiento y la utilización de la 
-- coma.
--------------------------------------------------------------------------------

library ieee ;
    use ieee.std_logic_1164.all ;
    use ieee.numeric_std.all ;

entity mult_by_constant is
  generic (
          DATA_IN_WIDTH     : integer := 16;
          DATA_OUT_WIDTH    : integer := 32;
          CONST_VALUE       : integer := 1
      );

  port (
        clk_i             : IN std_logic;
        reset_ni          : IN std_logic;
        data_i            : IN  std_logic_vector(DATA_IN_WIDTH-1 downto 0);
        data_o            : OUT std_logic_vector(DATA_OUT_WIDTH-1 downto 0)
    );
end entity ; -- mult_by_constant

architecture rtl of mult_by_constant is

signal temp : integer;

begin

temp <= to_integer(signed(data_i));

data_o <= std_logic_vector(to_signed(CONST_VALUE *temp,32));

end architecture ; -- rtl