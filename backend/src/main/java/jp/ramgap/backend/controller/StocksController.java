package jp.ramgap.backend.controller;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

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
import org.springframework.web.bind.annotation.RestController;

import jp.ramgap.backend.form.StocksAddForm;

@RestController
@RequestMapping("/api/stocks")
@CrossOrigin(origins = "http://localhost:3000") // React側のURLを許可
public class StocksController {
    private final List<StocksAddForm> stocks = new ArrayList<>();

    private final MessageSource messageSource;
    
    public StocksController(MessageSource messageSource) {
        this.messageSource = messageSource;
    }

    @PostMapping
    public ResponseEntity<String> postStocks(@Validated @RequestBody StocksAddForm stocksAddForm, BindingResult bindingResult, Locale locale) {
        if (bindingResult.hasErrors()) {
            StringBuilder errorMessage = new StringBuilder();
            for (ObjectError error : bindingResult.getAllErrors()) {
                String message = messageSource.getMessage(error, locale);
                errorMessage.append(message).append("; ");
            }
            return ResponseEntity.badRequest().body(errorMessage.toString());
        }
        
        stocks.add(stocksAddForm);

        return ResponseEntity.ok("Stock info added successfully!");
    }

    @GetMapping
    public List<StocksAddForm> getStocks() {
        return stocks;
    }

}
