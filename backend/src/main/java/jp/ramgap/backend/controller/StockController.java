package jp.ramgap.backend.controller;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import org.modelmapper.ModelMapper;
import org.springframework.context.MessageSource;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.ObjectError;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import jp.ramgap.backend.domain.stock.model.Stock;
import jp.ramgap.backend.domain.stock.service.StockService;
import jp.ramgap.backend.form.StockAddForm;

@RestController
@RequestMapping("/api/stocks")
@CrossOrigin(origins = "http://localhost:3000") // React側のURLを許可
public class StockController {
    private final List<StockAddForm> stocks = new ArrayList<>();

    private final MessageSource messageSource;

    private final StockService stockService;

    private final ModelMapper modelMapper;

    public StockController(MessageSource messageSource, StockService stockService, ModelMapper modelMapper) {
        this.messageSource = messageSource;
        this.stockService = stockService;
        this.modelMapper = modelMapper;
    }

    @PostMapping
    public ResponseEntity<String> postStocks(@Validated @RequestBody StockAddForm stockAddForm,
            BindingResult bindingResult, Locale locale) {
        if (bindingResult.hasErrors()) {
            StringBuilder errorMessage = new StringBuilder();
            for (ObjectError error : bindingResult.getAllErrors()) {
                String message = messageSource.getMessage(error, locale);
                errorMessage.append(message).append("; ");
            }
            return ResponseEntity.badRequest().body(errorMessage.toString());
        }

        // stocks.add(stockAddForm);

        Stock stock = modelMapper.map(stockAddForm, Stock.class);

        stockService.addStock(stock);

        return ResponseEntity.ok("Stock info added successfully!");
    }

    @GetMapping
    // public List<StockAddForm> getStocks() {
    // return stocks;
    public List<Stock> getStocks(@RequestParam int userId) {
        return stockService.getStocksByUserId(userId);
    }

}
