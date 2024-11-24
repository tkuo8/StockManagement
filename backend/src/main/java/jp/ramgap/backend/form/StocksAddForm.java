package jp.ramgap.backend.form;

import java.math.BigDecimal;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Digits;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class StocksAddForm {

    @NotBlank
    @Size(min = 4, max = 4, message = "{Size.stock.symbol}")
    private String symbol;

    @NotNull
    @PositiveOrZero
    @Digits(integer = 8, fraction = 2)
    @DecimalMax(value = "99999999.99", inclusive = true)
    @DecimalMin(value = "00000000.00", inclusive = true)
    private BigDecimal purchasePrice;

    @NotNull
    @PositiveOrZero
    private Integer quantity;

    @NotNull
    @PositiveOrZero
    @Digits(integer = 8, fraction = 2)
    @DecimalMax(value = "99999999.99", inclusive = true)
    @DecimalMin(value = "00000000.00", inclusive = true)
    private BigDecimal targetPrice;

    @NotNull
    @PositiveOrZero
    @Digits(integer = 8, fraction = 2)
    @DecimalMax(value = "99999999.99", inclusive = true)
    @DecimalMin(value = "00000000.00", inclusive = true)
    private BigDecimal cutLossPrice;
}
